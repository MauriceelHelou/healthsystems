#!/usr/bin/env python3
"""
Marketing Page Batch Generator

Uses Anthropic Batch API to generate all marketing page components in parallel.
Each component is a complete React TypeScript file with Framer Motion animations.

Usage:
    python generate_marketing_batch.py [--submit] [--poll BATCH_ID] [--retrieve BATCH_ID]

    --submit: Create and submit the batch request
    --poll BATCH_ID: Check status of a batch
    --retrieve BATCH_ID: Download results from completed batch
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

import anthropic

# =============================================================================
# DESIGN SYSTEM PROMPT (shared across all components)
# =============================================================================

DESIGN_SYSTEM_PROMPT = """You are an expert React/TypeScript developer creating marketing page components for HealthSystems Platform - a decision support tool for quantifying structural health interventions.

## Design System Contract

### Technology Stack
- React 18 with TypeScript (strict mode)
- TailwindCSS for styling (already configured)
- Framer Motion for animations (import from 'framer-motion')
- cn() utility from '@/utils/classNames' for class merging

### Color Palette (use these exact values)
```
Primary Blue: #0ea5e9 (primary-500) - CTAs, links, interactive
Secondary Purple: #a855f7 (secondary-500) - Accents
Orange: #FB923C - Highlights, emphasis
Text Primary: #1F2937 (gray-800) - Headings
Text Secondary: #4B5563 (gray-600) - Body text
Text Tertiary: #6B7280 (gray-500) - Captions
Background: #FFFFFF (white), #F9FAFB (gray-50 for alternating)
```

### Typography
- Font: Inter (already configured via Tailwind)
- Headings: `text-4xl md:text-5xl lg:text-6xl font-semibold tracking-tight text-gray-900`
- Subheadings: `text-xl md:text-2xl font-medium text-gray-600`
- Body: `text-base md:text-lg text-gray-600 leading-relaxed`

### Animation Conventions (Framer Motion)
```typescript
// Standard entrance animation
const fadeInUp = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.6, ease: "easeOut" } }
};

// Stagger children
const staggerContainer = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { staggerChildren: 0.1, delayChildren: 0.2 } }
};

// Use whileInView for scroll triggers
<motion.div
  initial="hidden"
  whileInView="visible"
  viewport={{ once: true, margin: "-100px" }}
  variants={fadeInUp}
>
```

### Stripe-Inspired Design Principles
1. Generous whitespace: Use `py-24 md:py-32` for section padding
2. Subtle shadows: `shadow-sm` on cards, `hover:shadow-lg` on hover
3. Micro-interactions: `hover:scale-[1.02]` with `transition-all duration-300`
4. Clean gradients: Use `bg-gradient-to-br` sparingly
5. Card borders: `border border-gray-200` with `rounded-2xl`
6. Max content width: `max-w-7xl mx-auto px-4 sm:px-6 lg:px-8`

### Accessibility Requirements
- All interactive elements must be keyboard accessible
- Use semantic HTML (section, article, nav, etc.)
- Include aria-labels where needed
- Support prefers-reduced-motion via Framer Motion's useReducedMotion
- Minimum touch target: 44x44px

### Component Structure
```typescript
'use client';

import { motion, useReducedMotion } from 'framer-motion';
import { cn } from '@/utils/classNames';

// Types at top
interface ComponentProps {
  className?: string;
}

// Animation variants
const variants = { ... };

// Main component (named export)
export function ComponentName({ className }: ComponentProps) {
  const shouldReduceMotion = useReducedMotion();

  return (
    <section className={cn("py-24 md:py-32", className)}>
      {/* content */}
    </section>
  );
}
```

### Project Context
HealthSystems Platform helps:
- State health departments allocate billions strategically
- Foundations optimize portfolios across geographies
- Community organizations quantify structural work impact

Key features:
- 400+ nodes, 2000+ mechanisms mapping causal pathways
- LLM-synthesized evidence from literature
- Equity-centered analysis with population stratification
- Real-time scenario modeling

Target users:
- State Health Department Directors
- Foundation Portfolio Directors
- Community Organization Leaders

OUTPUT FORMAT: Return ONLY the TypeScript/React code. No markdown, no explanations, just the complete .tsx file content that can be saved directly."""


# =============================================================================
# SECTION-SPECIFIC PROMPTS
# =============================================================================

SECTION_PROMPTS = {
    "hero": """Create a HeroSection component for the marketing home page.

## Content
- Headline: "Quantify How Policy Shapes Health"
- Subheadline: "A decision support platform that maps how structural interventions—housing policy, Medicaid design, workforce development—cascade through causal pathways to affect health outcomes."
- Primary CTA: "Explore the Map" (links to /systems)
- Secondary CTA: "Learn More" (scrolls to about section)

## Layout Requirements
- Full viewport height on desktop (min-h-screen), auto on mobile
- Content left-aligned, max-w-2xl
- Leave space on right for future animated visual
- Responsive: stack vertically on mobile

## Visual Elements
- Animated gradient text on "Policy" word (optional, use CSS animation)
- Subtle floating dots/particles in background (use CSS, not canvas)
- Two CTA buttons: primary (filled blue) and secondary (outline)

## Animations
- Staggered text reveal on mount (headline, then subheadline, then CTAs)
- Buttons: scale up slightly on hover with shadow increase
- Background elements: gentle floating animation

## Props Interface
```typescript
interface HeroSectionProps {
  onPrimaryCTA?: () => void;
  onSecondaryCTA?: () => void;
  className?: string;
}
```""",

    "about": """Create an AboutSection component for the marketing home page.

## Content

### Mission Statement
"Enable evidence-based decision-making for structural health interventions by making complex causal pathways visible, quantifiable, and actionable."

### Three Core Values (with icons - use emoji or simple SVG)
1. **Transparency** - "Every projection traces back to source studies. No black boxes."
2. **Equity** - "Outcomes stratified by population. See who benefits, who bears costs."
3. **Evidence** - "2000+ mechanisms derived from peer-reviewed literature."

### What Makes Us Different
"Unlike traditional health impact assessments that take months and produce qualitative reports, HealthSystems delivers quantified projections in seconds—all auditable to source research."

## Layout
- Alternating background: gray-50
- Mission statement centered with large text
- Three value cards in responsive grid (1 col mobile, 3 col desktop)
- "What makes us different" as a highlighted callout box

## Animations
- Section fades in on scroll
- Value cards stagger in from bottom
- Callout box slides in from right

## Props Interface
```typescript
interface AboutSectionProps {
  className?: string;
}
```""",

    "features": """Create a FeaturesSection component for the marketing home page.

## Content - 6 Feature Cards

1. **Interactive Systems Mapping**
   Icon: 🗺️ or network icon
   Description: "Visualize 400+ nodes and 2000+ mechanisms showing how structural conditions connect to health outcomes."

2. **LLM-Synthesized Evidence**
   Icon: 🤖 or brain icon
   Description: "Mechanisms extracted from literature using Claude AI, with full audit trail from studies to projections."

3. **Structural Competency Framework**
   Icon: 🏛️ or building icon
   Description: "Focus on root causes—policy, housing, economics—not individual behavior. Explicit equity lens throughout."

4. **Real-Time Scenario Modeling**
   Icon: ⚡ or lightning icon
   Description: "Seconds-to-answers analysis. 'What if we shift $50M to this intervention?' See results instantly."

5. **Equity-Centered Analysis**
   Icon: ⚖️ or balance icon
   Description: "Every projection stratified by race, SES, insurance status. Identify what reduces disparities."

6. **Transparent Assumptions**
   Icon: 🔍 or magnifying glass icon
   Description: "Click any number to see source studies. Challenge assumptions, propose improvements."

## Layout
- Section title: "What We Can Do"
- Subtitle: "Built for policymakers, foundations, and community organizations"
- 6 cards in responsive grid: 1 col mobile, 2 col tablet, 3 col desktop
- Each card: icon (large), title (bold), description

## Card Interactions
- Hover: lift up slightly (translateY -4px), increase shadow
- Optional: subtle border glow on hover using box-shadow
- 3D tilt effect on mouse move (using CSS transforms, not libraries)

## Animations
- Section title fades in
- Cards stagger in with 0.1s delay each

## Props Interface
```typescript
interface FeaturesSectionProps {
  className?: string;
}
```""",

    "how-to-use": """Create a HowToUseSection component for the marketing home page.

## Content - 4 Steps

1. **Select Your Geography**
   Description: "Choose a state, county, or city. The system automatically adapts to local policy context—Medicaid rules, housing protections, workforce programs."

2. **Identify Health Outcome**
   Description: "Pick the crisis you're trying to prevent: cardiovascular events, alcohol-related mortality, housing instability, or 50+ other outcomes."

3. **Explore Pathways**
   Description: "See which structural interventions matter most. Click nodes to understand mechanisms. Compare alternatives side-by-side."

4. **Model Scenarios**
   Description: "Ask 'what if' questions. Shift resources between interventions. See projected outcomes with confidence intervals."

## Layout
- Section title: "How It Works"
- Subtitle: "From question to evidence-based insight in minutes"
- Vertical timeline on mobile, horizontal on desktop
- Each step: number badge, title, description
- Connecting line between steps (animated on scroll)

## Visual Elements
- Step numbers in circular badges (1, 2, 3, 4)
- Dashed or solid line connecting steps
- Optional: small illustration/icon for each step

## Animations
- Steps reveal sequentially as user scrolls
- Connecting line draws progressively
- Number badges pop in with scale animation

## CTA at bottom
- "Try it now" button linking to /systems

## Props Interface
```typescript
interface HowToUseSectionProps {
  onTryNow?: () => void;
  className?: string;
}
```""",

    "roadmap": """Create a RoadmapSection component for the marketing home page.

## Content - 3 Phases

### Phase 1: MVP (Current) ✓
Status: Complete
Title: "Topology & Direction Discovery"
Features:
- 2000 mechanisms identified and catalogued
- 400+ nodes defined with specifications
- Direction of each mechanism (positive/negative)
- Literature lineage for every pathway

### Phase 2: Coming Soon
Status: In Progress
Title: "Quantification & Modeling"
Features:
- Effect size quantification with 95% confidence intervals
- Meta-analytic pooling from 300+ studies per mechanism
- Bayesian uncertainty propagation
- Intervention impact calculator

### Phase 3: Future
Status: Planned
Title: "Actor Network & Scale"
Features:
- Multi-geography deployment (50+ states/counties)
- Organizational collaboration mapping
- Real-time data integration
- Policy change alerts

## Layout
- Section title: "What We're Building"
- Subtitle: "A phased approach to comprehensive health systems modeling"
- Timeline visualization: vertical on mobile, horizontal on desktop
- Each phase: status badge, title, feature list
- Current phase highlighted with accent color

## Visual Elements
- Timeline line with dots/markers at each phase
- Status badges: "Complete" (green), "In Progress" (orange), "Planned" (gray)
- Checkmarks for completed features

## Animations
- Timeline line draws on scroll
- Phase cards fade in sequentially
- Status badges pop with scale effect

## Props Interface
```typescript
interface RoadmapSectionProps {
  className?: string;
}
```""",

    "team": """Create a TeamSection component for the marketing home page.

## Content - 4 Placeholder Team Members

1. **Dr. Sarah Chen** (PLACEHOLDER)
   Role: "Principal Investigator"
   Bio: "Professor of Population Health Sciences with 15 years of experience in health equity research and systems modeling."
   Image: Use a placeholder gradient or initials avatar

2. **Dr. Marcus Johnson** (PLACEHOLDER)
   Role: "Director of Data Science"
   Bio: "Former CDC epidemiologist specializing in causal inference and machine learning applications in public health."
   Image: Placeholder

3. **Dr. Elena Rodriguez** (PLACEHOLDER)
   Role: "Community Engagement Lead"
   Bio: "Community health advocate with deep expertise in translating research into actionable policy recommendations."
   Image: Placeholder

4. **Dr. James Park** (PLACEHOLDER)
   Role: "Technical Architect"
   Bio: "Full-stack engineer with background in health informatics and decision support systems."
   Image: Placeholder

## Layout
- Section title: "Our Team"
- Subtitle: "Researchers, engineers, and advocates working to transform health policy"
- 4 cards in responsive grid: 1 col mobile, 2 col tablet, 4 col desktop
- Each card: avatar, name, role, bio
- Social links placeholders (LinkedIn, Twitter icons)

## Card Design
- Avatar: circular, 80px on mobile, 120px on desktop
- Use gradient backgrounds for placeholder avatars (different colors)
- Name: bold, larger text
- Role: uppercase, small, primary color
- Bio: smaller text, gray

## Animations
- Cards fade in with stagger
- Hover: slight lift and shadow increase
- Avatar: subtle scale on hover

## Props Interface
```typescript
interface TeamSectionProps {
  className?: string;
}

// Export team data type for easy updates
export interface TeamMember {
  id: string;
  name: string;
  role: string;
  bio: string;
  image?: string;
  linkedin?: string;
  twitter?: string;
}
```""",

    "testimonials": """Create a TestimonialsSection component for the marketing home page.

## Content - 3 Placeholder Testimonials

1. **State Health Department**
   Quote: "For the first time, we can show our legislature exactly which interventions prevent the most health crises—and for whom. This changes how we justify our $800M budget."
   Attribution: "— Dr. Amanda Foster" (PLACEHOLDER)
   Title: "Director of Population Health"
   Organization: "State Health Department"

2. **Foundation**
   Quote: "We fund 50 programs across 5 states. Now we can finally compare apples to apples and understand which investments create the most equitable outcomes."
   Attribution: "— Michael Torres" (PLACEHOLDER)
   Title: "VP of Health Initiatives"
   Organization: "Community Foundation"

3. **Community Organization**
   Quote: "Our housing advocacy work saves lives—we always knew it, but couldn't prove it in terms funders understand. Now we can compete with clinical interventions for resources."
   Attribution: "— Rev. Patricia Williams" (PLACEHOLDER)
   Title: "Executive Director"
   Organization: "Community Health Alliance"

## Layout
- Section title: "What People Are Saying"
- Alternating background (gray-50)
- 3 testimonial cards in horizontal scroll on mobile, grid on desktop
- Large quotation marks as visual element

## Card Design
- Large opening quotation mark (decorative, light gray or primary-100)
- Quote text in larger, slightly italic font
- Attribution below with name, title, org
- Optional: org logo placeholder

## Animations
- Cards fade in with stagger
- Subtle auto-rotation option (carousel) - but also allow manual navigation
- Dots indicator for current testimonial on mobile

## Props Interface
```typescript
interface TestimonialsSectionProps {
  className?: string;
}

export interface Testimonial {
  id: string;
  quote: string;
  name: string;
  title: string;
  organization: string;
  image?: string;
}
```""",

    "footer-cta": """Create a FooterCTASection component for the marketing home page.

## Content

### Main CTA Area
- Headline: "Ready to transform how you approach health equity?"
- Subheadline: "Join state health departments, foundations, and community organizations already using evidence-based systems thinking."
- Primary CTA: "Get Started" (links to /systems)
- Secondary CTA: "Contact Us" (mailto or contact form)

### Footer Links (4 columns)
1. **Product**
   - Systems Map
   - Documentation
   - API Access
   - Changelog

2. **Research**
   - Methodology
   - Publications
   - Data Sources
   - Mechanism Bank

3. **Community**
   - GitHub
   - Discussions
   - Contributing
   - Code of Conduct

4. **Legal**
   - Privacy Policy
   - Terms of Service
   - Data License
   - Accessibility

### Bottom Bar
- Copyright: "© 2024 HealthSystems Platform. Built with evidence."
- Social links: GitHub, Twitter/X, LinkedIn (icon buttons)

## Layout
- CTA section: centered, generous padding, subtle gradient background
- Footer links: 4 column grid (stack on mobile)
- Bottom bar: flex between copyright and social icons
- Full width, darker background for footer (gray-900 or similar dark)

## Visual Elements
- CTA section: subtle gradient from primary-50 to white
- Footer: dark background with light text
- Social icons: circular buttons with hover effect

## Animations
- CTA section fades in on scroll
- Buttons have hover scale and glow effects
- Social icons have hover color change

## Props Interface
```typescript
interface FooterCTASectionProps {
  onGetStarted?: () => void;
  onContact?: () => void;
  className?: string;
}
```""",

    "home-page": """Create the main HomePage component that assembles all marketing sections.

## Component Imports
Import these section components (assume they exist):
- HeroSection from './sections/HeroSection'
- AboutSection from './sections/AboutSection'
- FeaturesSection from './sections/FeaturesSection'
- HowToUseSection from './sections/HowToUseSection'
- RoadmapSection from './sections/RoadmapSection'
- TeamSection from './sections/TeamSection'
- TestimonialsSection from './sections/TestimonialsSection'
- FooterCTASection from './sections/FooterCTASection'

## Layout
- Full page scroll with snap points (optional, can be disabled)
- Alternating section backgrounds (white, gray-50, white, etc.)
- Smooth scroll behavior enabled
- Fixed navigation header (assume exists elsewhere)

## Navigation
- Implement smooth scroll to sections when internal links clicked
- Each section should have an id for anchor linking:
  - #hero
  - #about
  - #features
  - #how-to-use
  - #roadmap
  - #team
  - #testimonials
  - #contact (footer CTA)

## Event Handlers
- onPrimaryCTA (hero): navigate to /systems
- onSecondaryCTA (hero): scroll to #about
- onTryNow (how-to-use): navigate to /systems
- onGetStarted (footer): navigate to /systems
- onContact (footer): open mailto or modal

## Performance
- Lazy load sections below the fold (optional)
- Use React.memo for sections that don't need re-renders

## Props Interface
```typescript
interface HomePageProps {
  // Optional: control which sections to show
}
```

## Additional Features
- Optional: scroll progress indicator at top
- Optional: floating "back to top" button after scrolling
- Meta tags for SEO (title, description) - add comments for where these go"""
}


# =============================================================================
# BATCH REQUEST BUILDER
# =============================================================================

def build_batch_requests() -> list[dict[str, Any]]:
    """Build the batch request payload for all marketing components."""
    requests = []

    for section_id, section_prompt in SECTION_PROMPTS.items():
        request = {
            "custom_id": f"marketing-{section_id}",
            "params": {
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 8192,
                "system": DESIGN_SYSTEM_PROMPT,
                "messages": [
                    {
                        "role": "user",
                        "content": section_prompt
                    }
                ]
            }
        }
        requests.append(request)

    return requests


def submit_batch(client: anthropic.Anthropic) -> str:
    """Submit the batch request and return the batch ID."""
    requests = build_batch_requests()

    print(f"Submitting batch with {len(requests)} requests...")
    print("Sections:", [r["custom_id"] for r in requests])

    batch = client.messages.batches.create(requests=requests)

    print(f"\n✓ Batch created successfully!")
    print(f"  Batch ID: {batch.id}")
    print(f"  Status: {batch.processing_status}")
    print(f"  Created: {batch.created_at}")

    return batch.id


def poll_batch(client: anthropic.Anthropic, batch_id: str) -> dict:
    """Poll batch status until completion."""
    print(f"Polling batch {batch_id}...")

    while True:
        batch = client.messages.batches.retrieve(batch_id)
        status = batch.processing_status
        counts = batch.request_counts

        print(f"  Status: {status}")
        print(f"  Succeeded: {counts.succeeded}, Errored: {counts.errored}, Processing: {counts.processing}")

        if status == "ended":
            print("\n✓ Batch processing complete!")
            return {
                "id": batch.id,
                "status": status,
                "succeeded": counts.succeeded,
                "errored": counts.errored,
                "results_url": getattr(batch, 'results_url', None)
            }

        if status == "failed":
            print("\n✗ Batch processing failed!")
            return {"id": batch.id, "status": status, "error": "Batch failed"}

        print("  Waiting 30 seconds...")
        time.sleep(30)


def retrieve_results(client: anthropic.Anthropic, batch_id: str, output_dir: Path):
    """Retrieve results and save to files."""
    print(f"Retrieving results for batch {batch_id}...")

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    sections_dir = output_dir / "sections"
    sections_dir.mkdir(exist_ok=True)

    # Map custom_id to filename
    filename_map = {
        "marketing-hero": "HeroSection.tsx",
        "marketing-about": "AboutSection.tsx",
        "marketing-features": "FeaturesSection.tsx",
        "marketing-how-to-use": "HowToUseSection.tsx",
        "marketing-roadmap": "RoadmapSection.tsx",
        "marketing-team": "TeamSection.tsx",
        "marketing-testimonials": "TestimonialsSection.tsx",
        "marketing-footer-cta": "FooterCTASection.tsx",
        "marketing-home-page": "HomePage.tsx",
    }

    results = []
    for result in client.messages.batches.results(batch_id):
        custom_id = result.custom_id
        result_type = result.result.type

        print(f"\n  Processing: {custom_id} (type: {result_type})")

        if result_type == "succeeded":
            content = result.result.message.content[0].text

            # Clean up the content (remove markdown code blocks if present)
            if content.startswith("```"):
                lines = content.split("\n")
                # Remove first line (```typescript or similar) and last line (```)
                content = "\n".join(lines[1:-1]) if lines[-1].strip() == "```" else "\n".join(lines[1:])

            filename = filename_map.get(custom_id, f"{custom_id}.tsx")

            # HomePage goes in root, others go in sections/
            if custom_id == "marketing-home-page":
                filepath = output_dir / filename
            else:
                filepath = sections_dir / filename

            filepath.write_text(content)
            print(f"  ✓ Saved: {filepath}")
            results.append({"custom_id": custom_id, "status": "success", "file": str(filepath)})
        elif result_type == "errored":
            error_info = result.result.error
            error_type = getattr(error_info, 'type', 'unknown')
            error_message = getattr(error_info, 'message', str(error_info))
            print(f"  ✗ Errored: {custom_id}")
            print(f"    Type: {error_type}")
            print(f"    Message: {error_message}")
            results.append({
                "custom_id": custom_id,
                "status": "errored",
                "error_type": error_type,
                "error_message": error_message
            })
        else:
            print(f"  ? Unknown result type: {result_type}")
            results.append({"custom_id": custom_id, "status": result_type, "raw": str(result)})

    # Save results summary
    summary_path = output_dir / "generation_summary.json"
    summary_path.write_text(json.dumps(results, indent=2))
    print(f"\n✓ Summary saved to: {summary_path}")

    return results


def save_batch_request_json(output_path: Path):
    """Save the batch request JSON for manual submission if needed."""
    requests = build_batch_requests()
    payload = {"requests": requests}

    output_path.write_text(json.dumps(payload, indent=2))
    print(f"✓ Batch request JSON saved to: {output_path}")


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="Generate marketing page components via Anthropic Batch API")
    parser.add_argument("--submit", action="store_true", help="Submit a new batch")
    parser.add_argument("--poll", metavar="BATCH_ID", help="Poll status of existing batch")
    parser.add_argument("--retrieve", metavar="BATCH_ID", help="Retrieve results from completed batch")
    parser.add_argument("--save-json", action="store_true", help="Save batch request JSON (for manual submission)")
    parser.add_argument("--output", default="../frontend/src/pages/marketing", help="Output directory for generated files")

    args = parser.parse_args()

    # Resolve output directory
    script_dir = Path(__file__).parent
    output_dir = (script_dir / args.output).resolve()

    # Initialize client
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key and (args.submit or args.poll or args.retrieve):
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key) if api_key else None

    if args.save_json:
        json_path = script_dir / "marketing_batch_request.json"
        save_batch_request_json(json_path)
        return

    if args.submit:
        batch_id = submit_batch(client)
        print(f"\nTo check status: python {__file__} --poll {batch_id}")
        print(f"To get results:  python {__file__} --retrieve {batch_id}")
        return

    if args.poll:
        result = poll_batch(client, args.poll)
        print(json.dumps(result, indent=2))
        return

    if args.retrieve:
        retrieve_results(client, args.retrieve, output_dir)
        return

    # Default: show help
    parser.print_help()
    print("\n\nExample workflow:")
    print("  1. python generate_marketing_batch.py --submit")
    print("  2. python generate_marketing_batch.py --poll <BATCH_ID>")
    print("  3. python generate_marketing_batch.py --retrieve <BATCH_ID>")


if __name__ == "__main__":
    main()
