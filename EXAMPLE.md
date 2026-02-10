# Example: AI-Powered Code Review Tools

## Input
```json
{
  "topic": "AI-powered code review tools for developers",
  "word_count": 1000,
  "language": "English"
}
```

## Output

### Article
**Title:** AI-Powered Code Review Tools: Streamlining Development in 2024

**Content:** (Markdown format with H1, H2, H3 structure)
```markdown
# AI-Powered Code Review Tools: Streamlining Development in 2024

## Introduction
In the fast-paced world of software development, quality and efficiency are paramount...

## What are AI-Powered Code Review Tools?
At their core, AI-powered code review tools leverage machine learning...

## Key Features & Capabilities
- Static Analysis
- Security Vulnerability Detection
- Code Style & Formatting Enforcement
...
```

### SEO Metadata
```json
{
  "title_tag": "AI-Powered Code Review Tools: Streamlining Development in 2024",
  "meta_description": "Explore AI-powered code review tools for developers. Learn about features, benefits, top tools, and how to integrate them into your workflow for improved code quality and faster development cycles.",
  "primary_keywords": [
    "AI code review tools",
    "code review",
    "software development",
    "machine learning",
    "static analysis"
  ],
  "secondary_keywords": [
    "developers",
    "code quality",
    "vulnerability detection",
    "security"
  ]
}
```

### Internal Links
```json
[
  {
    "anchor_text": "Understanding Static Analysis",
    "suggested_page": "/static-analysis"
  },
  {
    "anchor_text": "Best Practices for Code Quality",
    "suggested_page": "/code-quality-best-practices"
  }
]
```

### External References
```json
[
  {
    "source_name": "Forbes",
    "url": "https://www.forbes.com/sites/elizabethmcmichael/2023/07/27/ai-is-changing-the-way-developers-review-code/",
    "context": "Provides a high-level overview of the impact of AI on code reviews."
  },
  {
    "source_name": "G2",
    "url": "https://www.g2.com/categories/ai-code-review-tools",
    "context": "Offers a curated list of AI-powered code review tools with user reviews and comparisons."
  }
]
```

## Job Status Tracking

The system tracks job progress through these states:
1. **pending** - Job created, waiting to start
2. **running** - SERP analysis and article generation in progress
3. **completed** - Article successfully generated
4. **failed** - Error occurred (with error message)

Jobs are persisted to `jobs.json` and can be resumed if the process crashes.
