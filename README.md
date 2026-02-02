# AI News Aggregation Frontend

A sophisticated multi-agent frontend for news aggregation with WebRAG technology, built with Next.js and Tailwind CSS.

## Features

### 🤖 Multi-Agent Architecture
- **News Discovery** - Multi-site news search and discovery
- **Web Scraper** - Advanced content extraction with crawl4ai + BeautifulSoup
- **Content Classifier** - Entity classification and company tagging
- **AI Summarizer** - 30-40 word AI summaries with business focus
- **Data Exporter** - CSV, JSON, and ZIP export formats
- **Dashboard** - Central monitoring and management hub

### 🎨 Design System
- Glass morphism design with backdrop blur
- Animated gradient backgrounds
- Responsive layouts with Tailwind CSS
- Framer Motion animations
- Dark theme with purple/blue gradients

### 🛠️ Technology Stack
- **Framework**: Next.js 14 with App Router
- **Styling**: Tailwind CSS with custom animations
- **Components**: Radix UI primitives
- **Animations**: Framer Motion
- **Icons**: Lucide React
- **TypeScript**: Full type safety

## Getting Started

### Prerequisites
- Node.js 18+ 
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
```

2. Run the development server:
```bash
npm run dev
```

3. Open [http://localhost:3000](http://localhost:3000) in your browser.

### Build for Production

```bash
npm run build
npm start
```

## Project Structure

```
frontend/
├── src/
│   ├── app/                    # Next.js App Router pages
│   │   ├── globals.css         # Global styles and animations
│   │   ├── layout.tsx          # Root layout
│   │   ├── page.tsx            # Homepage
│   │   ├── dashboard/          # Dashboard page
│   │   ├── news-discoverer/    # News discovery agent
│   │   ├── web-scraper/        # Web scraping agent
│   │   ├── content-classifier/ # Classification agent
│   │   ├── ai-summarizer/      # Summarization agent
│   │   └── data-exporter/      # Export agent
│   ├── components/
│   │   └── ui/                 # Reusable UI components
│   ├── contexts/
│   │   └── SessionContext.tsx  # Session management
│   ├── types/
│   │   ├── NewsResponse.ts     # Type definitions
│   │   ├── ScrapingResponse.ts
│   │   ├── ClassificationResponse.ts
│   │   ├── SummarizationResponse.ts
│   │   └── ExportResponse.ts
│   └── lib/
│       └── utils.ts            # Utility functions
├── tailwind.config.js          # Tailwind configuration
├── tsconfig.json              # TypeScript configuration
├── next.config.js             # Next.js configuration
└── package.json               # Dependencies
```

## Styling System

### CSS Classes
- `.glass-card` - Glass morphism card effect
- `.button-primary` - Primary button style
- `.button-secondary` - Secondary button style
- `.gradient-text` - Animated gradient text
- `.metric-card` - Statistics card style

### Animations
- `float` - Gentle floating animation
- `glow` - Pulsing glow effect
- `pulse` - Subtle pulse animation
- `bounce-slow` - Slow bounce effect
- `spin-slow` - Slow rotation

### Color Palette
- **Primary**: Purple/Blue gradients
- **Background**: Dark (#171717)
- **Cards**: Semi-transparent black
- **Text**: White with varying opacity

## Agent Pages

Each agent page includes:
- Interactive forms with validation
- Real-time progress tracking
- Success/error state indicators
- Sample data loading for testing
- Responsive design

### API Integration

Pages are configured to communicate with backend APIs:
- `/api/news/discoverer`
- `/api/news/scraper`
- `/api/news/classifier`
- `/api/news/summarizer`
- `/api/news/exporter`

## Development Notes

### TypeScript Configuration
- Strict mode enabled
- Path aliases configured (`@/*`)
- Next.js types included

### Tailwind CSS
- Custom animations defined
- Extended color palette
- Responsive breakpoints
- Dark theme optimized

### Performance
- Optimized images and fonts
- Lazy loading components
- Efficient animations
- Minimal bundle size

## Deployment

### Vercel (Recommended)
1. Connect your GitHub repository
2. Configure build settings
3. Deploy automatically

### Docker
```bash
docker build -t news-aggregation-frontend .
docker run -p 3000:3000 news-aggregation-frontend
```

### Static Export
```bash
npm run build
npm run export
```

## Contributing

1. Follow the existing code style
2. Use TypeScript for all new code
3. Test responsive design
4. Update documentation as needed

## License

MIT License - see LICENSE file for details.
