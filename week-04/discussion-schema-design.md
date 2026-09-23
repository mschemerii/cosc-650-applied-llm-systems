# Week 4 Discussion: Schema Rigidity and Tool Calling

For this experiment, I designed a tool called `search_support_tickets` that queries an internal support-ticket database. I intentionally started with a loose schema:

```json
{
  "type": "object",
  "properties": {
    "status": {"type": "string"},
    "priority": {"type": "string"},
    "team": {"type": "string"},
    "topic": {"type": "string"},
    "days_back": {"type": "number"},
    "limit": {"type": "number"}
  }
}
```

I prompted the model: “Find the 10 highest-priority open AI-related support tickets from the last 30 days, assigned to the Facilities team.”

The loose test produced:

```json
{
  "status": "currently_open",
  "priority": "highest",
  "team": "Facilities",
  "topic": "artificial intelligence",
  "days_back": 30,
  "limit": 10
}
```

The output is understandable to a person but unreliable for a database API. `currently_open`, `highest`, and `artificial intelligence` are unconstrained values rather than values guaranteed to exist in the system. The loose schema also allows negative numbers, decimals, and unexpected additional fields.

I tightened the schema by requiring all important fields, adding enums, restricting numeric ranges, and rejecting unspecified properties:

```json
{
  "type": "object",
  "properties": {
    "status": {"type": "string", "enum": ["open", "closed", "pending"]},
    "priority": {"type": "string", "enum": ["low", "medium", "high", "critical"]},
    "team": {"type": "string", "enum": ["Facilities", "Sales", "Support"]},
    "topic": {"type": "string", "enum": ["AI", "billing", "software", "hardware"]},
    "days_back": {"type": "integer", "minimum": 1, "maximum": 365},
    "limit": {"type": "integer", "minimum": 1, "maximum": 100}
  },
  "required": ["status", "priority", "team", "topic", "days_back", "limit"],
  "additionalProperties": false
}
```

The tighter test produced:

```json
{
  "status": "open",
  "priority": "critical",
  "team": "Facilities",
  "topic": "AI",
  "days_back": 30,
  "limit": 10
}
```

The call is now structurally valid, but one semantic problem remains: “highest-priority” does not necessarily mean filter only for `critical`; it could mean retrieve matching tickets and sort them by priority. The schema prevents invalid values, but it cannot completely resolve user intent.

This suggests that rigid schemas are valuable for making tool calls predictable and executable, but excessive rigidity can encode the wrong interpretation. Constraints should enforce what the application knows must be valid while leaving ambiguous semantic decisions to the model or to explicit parameters such as `sort_by` and `sort_order`.

> Before posting, run the notebook with a live `GEMINI_API_KEY` and replace the two captured outputs above if the live model returns different arguments.
