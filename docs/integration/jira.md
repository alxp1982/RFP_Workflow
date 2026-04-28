# Jira Export

## Source
`outputs/stories.md` -- one Jira Story per Story, grouped under Epics.

## Jira issue structure
- **Issue type:** Epic (for Epics), Story (for Stories)
- **Summary:** `[<ID>] <title>`
- **Description:** user story + acceptance criteria + gherkin
- **Story Points:** S=1, M=3, L=5, XL=8
- **Labels:** `rfp-workflow`
- **Epic Link:** parent Epic summary

## Via Jira MCP
Use the instructions in `.agent/skills/rfp-export/skill.md` (Export C).

## Manually (CSV import)
Ask your AI assistant:
```
Convert outputs/stories.md to a Jira CSV import file.
Columns: Issue Type, Summary, Description, Story Points, Labels, Epic Link
```
Then use Jira -> Projects -> Import issues -> CSV.
