export interface ExportResponse {
  status: string;
  exported_count: number;
  format: string;
  filename?: string;
  download_url?: string;
  message: string;
  files_created?: string[];
}
