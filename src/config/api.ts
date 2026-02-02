// API Configuration
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const API_ENDPOINTS = {
  // Health and status
  HEALTH: `${API_BASE_URL}/api/health`,
  DASHBOARD_STATS: `${API_BASE_URL}/api/dashboard/stats`,
  
  // News processing endpoints
  NEWS_DISCOVERER: `${API_BASE_URL}/api/news/discoverer`,
  WEB_SCRAPER: `${API_BASE_URL}/api/news/scraper`,
  CONTENT_CLASSIFIER: `${API_BASE_URL}/api/news/classifier`,
  AI_SUMMARIZER: `${API_BASE_URL}/api/news/summarizer`,
  DATA_EXPORTER: `${API_BASE_URL}/api/news/exporter`,


  // Streamlit-equivalent endpoints
  SUMMARIZE: `${API_BASE_URL}/summarize`,
  CLASSIFY: `${API_BASE_URL}/classify`,
  WEBRAG_INGEST: `${API_BASE_URL}/webrag/ingest`,
  WEBRAG_QUERY: `${API_BASE_URL}/webrag/query`,
  
  // Task management
  TASK_STATUS: (taskId: string) => `${API_BASE_URL}/api/tasks/${taskId}`,
  TASK_RESULT: (taskId: string) => `${API_BASE_URL}/api/tasks/${taskId}/result`,
} as const;

// Helper function for API calls
export const apiCall = async (endpoint: string, options: RequestInit = {}) => {
  const url = endpoint.startsWith('http') ? endpoint : `${API_BASE_URL}${endpoint}`;
  
  const response = await fetch(url, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  });
  
  if (!response.ok) {
    throw new Error(`API Error: ${response.status} ${response.statusText}`);
  }
  
  return response.json();
};

// Helper for task-based operations
export const executeTask = async (endpoint: string, payload: any) => {
  const initialResponse = await apiCall(endpoint, {
    method: 'POST',
    body: JSON.stringify(payload),
  });
  
  if (initialResponse.task_id) {
    // Poll for task completion
    const pollForResults = async (): Promise<any> => {
      const status = await apiCall(API_ENDPOINTS.TASK_STATUS(initialResponse.task_id));
      
      if (status.status === 'completed') {
        return await apiCall(API_ENDPOINTS.TASK_RESULT(initialResponse.task_id));
      } else if (status.status === 'failed') {
        throw new Error(status.error || 'Task failed');
      } else {
        // Still running, wait and poll again
        await new Promise(resolve => setTimeout(resolve, 2000));
        return pollForResults();
      }
    };
    
    return pollForResults();
  }
  
  // Direct response (no task_id)
  return initialResponse;
};
