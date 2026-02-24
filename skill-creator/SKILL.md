---
name: skill-creator
description: Create or update AgentSkills. Use when designing, structuring, or publishing skills with references and assets. Triggers on requests like "create a skill", "build a skill for X", "publish this skill", or when the user wants to design, structure, or publish AgentSkills.
---

# Skill Creator

Guidance for creating effective AgentSkills.

## Getting Started

If you have no prior context of a conversation, this is likely a new session. Read this SKILL.md and follow the instructions inside to proceed with skill creation or modification.

## About Skills

Skills are modular, self-contained packages that extend AI capabilities by providing specialized knowledge, workflows, and tools. Think of them as "onboarding guides" for specific domains or tasks—they transform the AI from a general-purpose agent into a specialized agent equipped with procedural knowledge.

### What Skills Provide

1. **Specialized workflows** - Multi-step procedures for specific domains
2. **Tool integrations** - Instructions for working with specific file formats or APIs
3. **Domain expertise** - Company-specific knowledge, schemas, business logic
4. **Bundled resources** - References and assets for complex and repetitive tasks

## Core Principles

### Concise is Key

The context window is a public good. Skills share the context window with everything else the AI needs: system prompt, conversation history, other Skills' metadata, and the actual user request.

**Default assumption: The AI is already very smart.** Only add context the AI doesn't already have. Challenge each piece of information: "Does the AI really need this explanation?" and "Does this paragraph justify its token cost?"

Prefer concise examples over verbose explanations.

### Set Appropriate Degrees of Freedom

Match the level of specificity to the task's fragility and variability:

**High freedom (text-based instructions)**: Use when multiple approaches are valid, decisions depend on context, or heuristics guide the approach.

**Medium freedom (pseudocode with parameters)**: Use when a preferred pattern exists, some variation is acceptable, or configuration affects behavior.

**Low freedom (specific code, few parameters)**: Use when operations are fragile and error-prone, consistency is critical, or a specific sequence must be followed.

### Anatomy of a Skill

Every skill consists of a required SKILL.md file and optional bundled resources:

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter metadata (required)
│   │   ├── name: (required)
│   │   └── description: (required)
│   └── Markdown instructions (required)
└── Bundled Resources (optional)
    ├── references/       - Documentation intended to be loaded into context as needed
    └── assets/           - Files used in output (templates, icons, fonts, etc.)
```

#### SKILL.md (required)

Every SKILL.md consists of:

- **Frontmatter** (YAML): Contains `name` and `description` fields. These are the only fields that the AI reads to determine when the skill gets used, thus it is very important to be clear and comprehensive in describing what the skill is, and when it should be used.
- **Body** (Markdown): Instructions and guidance for using the skill. Only loaded AFTER the skill triggers (if at all).

#### Bundled Resources (optional)

##### References (`references/`)

Documentation and reference material intended to be loaded as needed into context to inform the AI's process and thinking.

- **When to include**: For documentation that the AI should reference while working
- **Examples**: `references/finance.md` for financial schemas, `references/mnda.md` for company NDA template, `references/policies.md` for company policies, `references/api_docs.md` for API specifications
- **Use cases**: Database schemas, API documentation, domain knowledge, company policies, detailed workflow guides
- **Benefits**: Keeps SKILL.md lean, loaded only when the AI determines it's needed
- **Best practice**: If files are large (>10k words), include grep search patterns in SKILL.md
- **Avoid duplication**: Information should live in either SKILL.md or references files, not both. Prefer references files for detailed information unless it's truly core to the skill—this keeps SKILL.md lean while making information discoverable without hogging the context window. Keep only essential procedural instructions and workflow guidance in SKILL.md; move detailed reference material, schemas, and examples to references files.

##### Assets (`assets/`)

Files not intended to be loaded into context, but rather used within the output the AI produces.

- **When to include**: When the skill needs files that will be used in the final output
- **Examples**: `assets/logo.png` for brand assets, `assets/slides.pptx` for PowerPoint templates, `assets/frontend-template/` for HTML/React boilerplate, `assets/font.ttf` for typography
- **Use cases**: Templates, images, icons, boilerplate code, fonts, sample documents that get copied or modified
- **Benefits**: Separates output resources from documentation, enables the AI to use files without loading them into context

#### What to Not Include in a Skill

A skill should only contain essential files that directly support its functionality. Do NOT create extraneous documentation or auxiliary files, including:

- README.md
- INSTALLATION_GUIDE.md
- QUICK_REFERENCE.md
- CHANGELOG.md
- etc.

The skill should only contain the information needed for an AI agent to do the job at hand. It should not contain auxiliary context about the process that went into creating it, setup and testing procedures, user-facing documentation, etc. Creating additional documentation files just adds clutter and confusion.

### Progressive Disclosure Design Principle

Skills use a three-level loading system to manage context efficiently:

1. **Metadata (name + description)** - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (<5k words)
3. **Bundled resources** - As needed by the AI (loaded selectively)

#### Progressive Disclosure Patterns

Keep SKILL.md body to the essentials and under 500 lines to minimize context bloat. Split content into separate files when approaching this limit. When splitting out content into other files, it is very important to reference them from SKILL.md and describe clearly when to read them, to ensure the reader of the skill knows they exist and when to use them.

**Key principle:** When a skill supports multiple variations, frameworks, or options, keep only the core workflow and selection guidance in SKILL.md. Move variant-specific details (patterns, examples, configuration) into separate reference files.

**Pattern 1: High-level guide with references**

```markdown
# PDF Processing

## Quick start

Extract text with pdfplumber:
[code example]

## Advanced features

- **Form filling**: See [FORMS.md](FORMS.md) for complete guide
- **API reference**: See [REFERENCE.md](REFERENCE.md) for all methods
- **Examples**: See [EXAMPLES.md](EXAMPLES.md) for common patterns
```

The AI loads FORMS.md, REFERENCE.md, or EXAMPLES.md only when needed.

**Pattern 2: Domain-specific organization**

For Skills with multiple domains, organize content by domain to avoid loading irrelevant context:

```
bigquery-skill/
├── SKILL.md (overview and navigation)
└── reference/
    ├── finance.md (revenue, billing metrics)
    ├── sales.md (opportunities, pipeline)
    ├── product.md (API usage, features)
    └── marketing.md (campaigns, attribution)
```

When a user asks about sales metrics, the AI only reads sales.md.

**Pattern 3: Conditional details**

Show basic content, link to advanced content:

```markdown
# DOCX Processing

## Creating documents

Use docx-js for new documents. See [DOCX-JS.md](DOCX-JS.md).

## Editing documents

For simple edits, modify the XML directly.

**For tracked changes**: See [REDLINING.md](REDLINING.md)
**For OOXML details**: See [OOXML.md](OOXML.md)
```

The AI reads REDLINING.md or OOXML.md only when the user needs those features.

**Important guidelines:**

- **Avoid deeply nested references** - Keep references one level deep from SKILL.md. All reference files should link directly from SKILL.md.
- **Structure longer reference files** - For files longer than 100 lines, include a table of contents at the top so the AI can see the full scope when previewing.

## Skill Creation Process

Skill creation involves these steps:

1. Understand the skill with concrete examples
2. Plan reusable skill contents (references, assets)
3. Initialize the skill (create directory and SKILL.md)
4. Edit the skill (implement resources and write SKILL.md)
5. Validate the skill (check structure and frontmatter)
6. Publish the skill (deploy to skills repository and push)
7. Iterate based on real usage

Follow these steps in order, skipping only if there is a clear reason why they are not applicable.

### Skill Naming

- Use lowercase letters, digits, and hyphens only; normalize user-provided titles to hyphen-case (e.g., "Plan Mode" -> `plan-mode`).
- When generating names, generate a name under 64 characters (letters, digits, hyphens).
- Prefer short, verb-led phrases that describe the action.
- Namespace by tool when it improves clarity or triggering (e.g., `gh-address-comments`, `linear-address-issue`).
- Name the skill folder exactly after the skill name.

### Step 1: Understanding the Skill with Concrete Examples

Skip this step only when the skill's usage patterns are already clearly understood. It remains valuable even when working with an existing skill.

To create an effective skill, clearly understand concrete examples of how the skill will be used. This understanding can come from either direct user examples or generated examples that are validated with user feedback.

For example, when building an image-editor skill, relevant questions include:

- "What functionality should the image-editor skill support? Editing, rotating, anything else?"
- "Can you give some examples of how this skill would be used?"
- "I can imagine users asking for things like 'Remove the red-eye from this image' or 'Rotate this image'. Are there other ways you imagine this skill being used?"
- "What would a user say that should trigger this skill?"

To avoid overwhelming users, avoid asking too many questions in a single message. Start with the most important questions and follow up as needed for better effectiveness.

Conclude this step when there is a clear sense of the functionality the skill should support.

### Step 2: Planning the Reusable Skill Contents

To turn concrete examples into an effective skill, analyze each example by:

1. Considering how to execute on the example from scratch
2. Identifying what references and assets would be helpful when executing these workflows repeatedly

Example: When building a `pdf-editor` skill to handle queries like "Help me rotate this PDF," the analysis shows:

1. Rotating a PDF requires knowledge of Python libraries like PyPDF2 or pikepdf
2. A `references/pdf-operations.md` file documenting the libraries and methods would be helpful

Example: When designing a `frontend-webapp-builder` skill for queries like "Build me a todo app" or "Build me a dashboard to track my steps," the analysis shows:

1. Writing a frontend webapp requires the same boilerplate HTML/React each time
2. An `assets/hello-world/` template containing the boilerplate HTML/React project files would be helpful to store in the skill

Example: When building a `big-query` skill to handle queries like "How many users have logged in today?" the analysis shows:

1. Querying BigQuery requires re-discovering the table schemas and relationships each time
2. A `references/schema.md` file documenting the table schemas would be helpful to store in the skill

To establish the skill's contents, analyze each concrete example to create a list of the reusable resources to include: references and assets.

### Step 3: Initializing the Skill

At this point, it is time to actually create the skill.

Skip this step only if the skill being developed already exists, and iteration or packaging is needed. In this case, continue to the next step.

When creating a new skill from scratch, create the skill directory structure manually:

1. **Create the skill directory** at the specified path with the skill name
2. **Create SKILL.md** with proper frontmatter and a template structure
3. **Create resource directories** (references/, assets/) only if needed

Use this SKILL.md template:

```markdown
---
name: {skill-name}
description: [Complete and informative explanation of what the skill does and when to use it. Include WHEN to use this skill - specific scenarios, file types, or tasks that trigger it.]
---

# {Skill Title}

## Overview

[1-2 sentences explaining what this skill enables]

## [Main Section - choose structure based on skill type]

### Workflow-Based (best for sequential processes)
- Works well when there are clear step-by-step procedures
- Structure: ## Overview -> ## Workflow Decision Tree -> ## Step 1 -> ## Step 2...

### Task-Based (best for tool collections)
- Works well when the skill offers different operations/capabilities  
- Structure: ## Overview -> ## Quick Start -> ## Task Category 1 -> ## Task Category 2...

### Reference/Guidelines (best for standards or specifications)
- Works well for brand guidelines, coding standards, or requirements
- Structure: ## Overview -> ## Guidelines -> ## Specifications -> ## Usage...

### Capabilities-Based (best for integrated systems)
- Works well when the skill provides multiple interrelated features
- Structure: ## Overview -> ## Core Capabilities -> ### 1. Feature -> ### 2. Feature...

[Add content here. Include code samples, decision trees, concrete examples with realistic user requests, and references to templates/references as needed]

## Resources (optional)

Create only the resource directories this skill actually needs. Delete this section if no resources are required.

### references/
Documentation and reference material intended to be loaded as needed into context.

### assets/
Files not intended to be loaded into context, but rather used within the output the AI produces.
```

After initialization, customize the SKILL.md and add resources as needed.

### Step 4: Edit the Skill

When editing the (newly-generated or existing) skill, remember that the skill is being created for another AI instance to use. Include information that would be beneficial and non-obvious to the AI. Consider what procedural knowledge, domain-specific details, or reusable assets would help another AI instance execute these tasks more effectively.

#### Learn Proven Design Patterns

Consult these helpful guides based on your skill's needs:

- **Multi-step processes**: See references/workflows.md for sequential workflows and conditional logic
- **Specific output formats or quality standards**: See references/output-patterns.md for template and example patterns

These files contain established best practices for effective skill design.

#### Start with Reusable Skill Contents

To begin implementation, start with the reusable resources identified above: `references/` and `assets/` files. Note that this step may require user input. For example, when implementing a `brand-guidelines` skill, the user may need to provide brand assets or templates to store in `assets/`, or documentation to store in `references/`.

Only create resource directories that are actually required.

#### Update SKILL.md

**Writing Guidelines:** Always use imperative/infinitive form.

##### Frontmatter

Write the YAML frontmatter with `name` and `description`:

- `name`: The skill name
- `description`: This is the primary triggering mechanism for your skill, and helps the AI understand when to use the skill.
  - Include both what the Skill does and specific triggers/contexts for when to use it.
  - Include all "when to use" information here - Not in the body. The body is only loaded after triggering, so "When to Use This Skill" sections in the body are not helpful to the AI.
  - Example description for a `docx` skill: "Comprehensive document creation, editing, and analysis with support for tracked changes, comments, formatting preservation, and text extraction. Use when the AI needs to work with professional documents (.docx files) for: (1) Creating new documents, (2) Modifying or editing content, (3) Working with tracked changes, (4) Adding comments, or any other document tasks"

Do not include any other fields in YAML frontmatter beyond `name` and `description` unless specifically needed.

##### Body

Write instructions for using the skill and its bundled resources.

### Step 5: Validating the Skill

Once development of the skill is complete, validate the skill structure before packaging:

**Validation Checklist:**

1. **SKILL.md exists**: The file must be present in the skill root directory
2. **YAML frontmatter format**: Must start with `---` and have valid YAML
3. **Required frontmatter fields**:
   - `name`: Must be present, hyphen-case (lowercase letters, digits, hyphens only)
   - `description`: Must be present, clear and comprehensive
4. **Name constraints**:
   - Maximum 64 characters
   - No leading/trailing hyphens
   - No consecutive hyphens
   - Only lowercase letters, digits, and hyphens
5. **Description constraints**:
   - Maximum 1024 characters
   - No angle brackets (`<` or `>`)
   - Should describe what the skill does AND when to use it
6. **Directory structure**: Skill folder name should match the `name` in frontmatter
7. **No extraneous files**: No README.md, CHANGELOG.md, etc.

Run these validation checks manually before proceeding to packaging.

### Step 6: Publishing the Skill

Once validation passes, publish the skill to the skills repository at `/Users/pcstyle/skills/`:

**Publishing Process:**

1. **Copy the skill directory** to `/Users/pcstyle/skills/{skill-name}/`
2. **Commit and push** the changes to the repository

```bash
# Copy skill to the skills repository
cp -r /path/to/skill/{skill-name} /Users/pcstyle/skills/{skill-name}

# Commit and push
cd /Users/pcstyle/skills
git add {skill-name}/
git commit -m "feat: add {skill-name} skill"
git push
```

**When updating an existing skill:**
```bash
# Overwrite existing skill in the repository
cp -r /path/to/skill/{skill-name} /Users/pcstyle/skills/{skill-name}

cd /Users/pcstyle/skills
git add {skill-name}/
git commit -m "feat: update {skill-name} skill"
git push
```

Always commit and push after adding or updating a skill.

### Step 7: Iterate

After testing the skill, users may request improvements. Often this happens right after using the skill, with fresh context of how the skill performed.

**Iteration workflow:**

1. Use the skill on real tasks
2. Notice struggles or inefficiencies
3. Identify how SKILL.md or bundled resources should be updated
4. Implement changes and test again
5. Re-validate and re-publish as needed
