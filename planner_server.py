 #!/opt/anaconda3/envs/spyder/bin/python
from mcp.server.fastmcp import FastMCP, Context
import os
import re
from datetime import datetime

# Create an MCP server
mcp = FastMCP("TaskPlanner")
# 修改为获取工作路径作为当前文件夹
PLAN_FILE = os.path.join(os.getcwd(), "plan.md")
def ensure_plan_file_exists():
    """Create the plan file if it doesn't exist."""
    if not os.path.exists(PLAN_FILE):
        with open(PLAN_FILE, "w", encoding="utf-8") as f:
            f.write("# Task Plan\n\nCreated on: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n\n## Steps\n\n")

@mcp.tool()
def think_and_plan(task_description: str, ctx: Context = None) -> str:
    """
    Think through a task and create a structured plan.
    
    Args:
        task_description: A description of the task to be planned
    
    Returns:
        A message indicating the plan was created
    """
    ensure_plan_file_exists()
    
    # Read existing content to avoid overwriting
    with open(PLAN_FILE, "r", encoding="utf-8") as f:
        existing_content = f.read()
    
    # Check if there's already a plan for this task
    if task_description in existing_content:
        return f"A plan for '{task_description}' already exists in {PLAN_FILE}."
    
    # Create a new plan section
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_plan = f"\n## {task_description}\n\nCreated: {timestamp}\n\n"
    new_plan += "### Planning Notes\n\nThis is a preliminary analysis of the task.\n\n"
    new_plan += "### Steps\n\n"
    new_plan += "[ ] Initialize planning\n"
    new_plan += "[ ] Analyze requirements\n"
    new_plan += "[ ] Design solution\n"
    
    # Write the plan to the file
    with open(PLAN_FILE, "a", encoding="utf-8") as f:
        f.write(new_plan)
    
    if ctx:
        ctx.info(f"Created new plan for: {task_description}")
    
    return f"Created new plan for '{task_description}' in {PLAN_FILE}. Review and customize the steps as needed."

@mcp.tool()
def add_step(step_description: str, task_title: str = None, ctx: Context = None) -> str:
    """
    Add a new step to the plan.
    
    Args:
        step_description: Description of the step to add
        task_title: The task title to add the step to (uses the latest task if not specified)
    
    Returns:
        A message indicating the step was added
    """
    ensure_plan_file_exists()
    
    with open(PLAN_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    
    # If no specific task, find the most recent task section
    if not task_title:
        task_sections = re.findall(r'## (.+?)\n', content)
        if not task_sections:
            return "No tasks found in the plan. Create a task first using think_and_plan."
        task_title = task_sections[-1]
    
    # Find the task section
    task_pattern = re.compile(rf'## {re.escape(task_title)}\n(.+?)(?=\n## |$)', re.DOTALL)
    task_match = task_pattern.search(content)
    
    if not task_match:
        return f"Task '{task_title}' not found in the plan."
    
    # Find the Steps section within the task
    task_content = task_match.group(0)
    steps_pattern = re.compile(r'### Steps\n\n(.*?)(?=\n### |$)', re.DOTALL)
    steps_match = steps_pattern.search(task_content)
    
    if not steps_match:
        # No Steps section found, add one
        updated_task = task_content + "\n### Steps\n\n[ ] " + step_description + "\n"
        updated_content = content.replace(task_content, updated_task)
    else:
        # Add to existing Steps section
        steps_section = steps_match.group(0)
        updated_steps = steps_section + "[ ] " + step_description + "\n"
        updated_task = task_content.replace(steps_section, updated_steps)
        updated_content = content.replace(task_content, updated_task)
    
    # Write back to file
    with open(PLAN_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)
    
    if ctx:
        ctx.info(f"Added step: {step_description} to task: {task_title}")
    
    return f"Added step '{step_description}' to task '{task_title}'."

@mcp.tool()
def mark_step_complete(step_text: str, task_title: str = None, ctx: Context = None) -> str:
    """
    Mark a step as completed in the plan.
    
    Args:
        step_text: Text of the step to mark as complete
        task_title: The task title containing the step (uses the latest task if not specified)
    
    Returns:
        A message indicating the step was marked as complete
    """
    ensure_plan_file_exists()
    
    with open(PLAN_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    
    # If no specific task, find the most recent task section
    if not task_title:
        task_sections = re.findall(r'## (.+?)\n', content)
        if not task_sections:
            return "No tasks found in the plan."
        task_title = task_sections[-1]
    
    # Find the task section
    task_pattern = re.compile(rf'## {re.escape(task_title)}\n(.+?)(?=\n## |$)', re.DOTALL)
    task_match = task_pattern.search(content)
    
    if not task_match:
        return f"Task '{task_title}' not found in the plan."
    
    # Look for the step and mark it as complete
    task_content = task_match.group(0)
    step_pattern = re.compile(rf'\[ \] {re.escape(step_text)}')
    
    if step_pattern.search(task_content):
        updated_task = step_pattern.sub(f'[✅] {step_text}', task_content)
        updated_content = content.replace(task_content, updated_task)
        
        # Write back to file
        with open(PLAN_FILE, "w", encoding="utf-8") as f:
            f.write(updated_content)
        
        if ctx:
            ctx.info(f"Marked step as complete: {step_text}")
        
        return f"Marked step '{step_text}' as complete in task '{task_title}'."
    else:
        return f"Step '{step_text}' not found in task '{task_title}'."

@mcp.tool()
def review_plan(task_title: str = None, ctx: Context = None) -> str:
    """
    Review the current plan and return its contents.
    
    Args:
        task_title: Specific task to review (reviews the entire plan if not specified)
    
    Returns:
        The current plan contents
    """
    ensure_plan_file_exists()
    
    with open(PLAN_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    
    if task_title:
        # Find the specific task section
        task_pattern = re.compile(rf'## {re.escape(task_title)}\n(.+?)(?=\n## |$)', re.DOTALL)
        task_match = task_pattern.search(content)
        
        if not task_match:
            return f"Task '{task_title}' not found in the plan."
        
        result = f"# Review of task: {task_title}\n\n" + task_match.group(0)
    else:
        result = content
    
    if ctx:
        ctx.info("Reviewed plan" + (f" for task: {task_title}" if task_title else ""))
    
    return result

@mcp.tool()
def add_issue(issue_description: str, step_text: str, task_title: str = None, ctx: Context = None) -> str:
    """
    Add an issue note to a specific step in the plan.
    
    Args:
        issue_description: Description of the issue
        step_text: The step text to add the issue to
        task_title: The task title (uses the latest task if not specified)
    
    Returns:
        A message indicating the issue was added
    """
    ensure_plan_file_exists()
    
    with open(PLAN_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    
    # If no specific task, find the most recent task section
    if not task_title:
        task_sections = re.findall(r'## (.+?)\n', content)
        if not task_sections:
            return "No tasks found in the plan."
        task_title = task_sections[-1]
    
    # Find the task section
    task_pattern = re.compile(rf'## {re.escape(task_title)}\n(.+?)(?=\n## |$)', re.DOTALL)
    task_match = task_pattern.search(content)
    
    if not task_match:
        return f"Task '{task_title}' not found in the plan."
    
    # Find the specific step
    task_content = task_match.group(0)
    step_pattern = re.compile(rf'(\[\S?\] {re.escape(step_text)})(.*?)(?=\n\[\S?\] |$)', re.DOTALL)
    step_match = step_pattern.search(task_content)
    
    if not step_match:
        return f"Step '{step_text}' not found in task '{task_title}'."
    
    # Add the issue note to the step
    step_content = step_match.group(0)
    issue_note = f"\n    - ⚠️ ISSUE: {issue_description}"
    
    if "⚠️ ISSUE:" in step_content:
        # There's already an issue, add this as another bullet point
        updated_step = step_content + issue_note
    else:
        # First issue for this step
        updated_step = step_content + issue_note
    
    updated_task = task_content.replace(step_content, updated_step)
    updated_content = content.replace(task_content, updated_task)
    
    # Write back to file
    with open(PLAN_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)
    
    if ctx:
        ctx.info(f"Added issue to step: {step_text}")
    
    return f"Added issue '{issue_description}' to step '{step_text}' in task '{task_title}'."

@mcp.tool()
def resolve_issue(step_text: str, resolution_text: str, task_title: str = None, ctx: Context = None) -> str:
    """
    Mark an issue as resolved for a specific step.
    
    Args:
        step_text: The step text containing the issue
        resolution_text: Description of how the issue was resolved
        task_title: The task title (uses the latest task if not specified)
    
    Returns:
        A message indicating the issue was resolved
    """
    ensure_plan_file_exists()
    
    with open(PLAN_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    
    # If no specific task, find the most recent task section
    if not task_title:
        task_sections = re.findall(r'## (.+?)\n', content)
        if not task_sections:
            return "No tasks found in the plan."
        task_title = task_sections[-1]
    
    # Find the task section
    task_pattern = re.compile(rf'## {re.escape(task_title)}\n(.+?)(?=\n## |$)', re.DOTALL)
    task_match = task_pattern.search(content)
    
    if not task_match:
        return f"Task '{task_title}' not found in the plan."
    
    # Find the specific step
    task_content = task_match.group(0)
    step_pattern = re.compile(rf'(\[\S?\] {re.escape(step_text)})(.*?)(?=\n\[\S?\] |$)', re.DOTALL)
    step_match = step_pattern.search(task_content)
    
    if not step_match:
        return f"Step '{step_text}' not found in task '{task_title}'."
    
    # Check if there are issues
    step_content = step_match.group(0)
    if "⚠️ ISSUE:" not in step_content:
        return f"No issues found for step '{step_text}' in task '{task_title}'."
    
    # Mark issues as resolved
    issue_pattern = re.compile(r'(    - ⚠️ ISSUE: .*?)(?=\n    - |$)', re.DOTALL)
    resolved_step = issue_pattern.sub(r'\1 (✓ RESOLVED: ' + resolution_text + ')', step_content)
    
    updated_task = task_content.replace(step_content, resolved_step)
    updated_content = content.replace(task_content, updated_task)
    
    # Write back to file
    with open(PLAN_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)
    
    if ctx:
        ctx.info(f"Resolved issue in step: {step_text}")
    
    return f"Marked issues as resolved in step '{step_text}' for task '{task_title}'."

@mcp.tool()
def update_planning_notes(notes: str, task_title: str = None, ctx: Context = None) -> str:
    """
    Update the planning notes for a task.
    
    Args:
        notes: The new planning notes
        task_title: The task title (uses the latest task if not specified)
    
    Returns:
        A message indicating the notes were updated
    """
    ensure_plan_file_exists()
    
    with open(PLAN_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    
    # If no specific task, find the most recent task section
    if not task_title:
        task_sections = re.findall(r'## (.+?)\n', content)
        if not task_sections:
            return "No tasks found in the plan."
        task_title = task_sections[-1]
    
    # Find the task section
    task_pattern = re.compile(rf'## {re.escape(task_title)}\n(.+?)(?=\n## |$)', re.DOTALL)
    task_match = task_pattern.search(content)
    
    if not task_match:
        return f"Task '{task_title}' not found in the plan."
    
    # Find the Planning Notes section
    task_content = task_match.group(0)
    notes_pattern = re.compile(r'### Planning Notes\n\n(.*?)(?=\n### |$)', re.DOTALL)
    notes_match = notes_pattern.search(task_content)
    
    if not notes_match:
        # No Planning Notes section found, add one
        updated_task = task_content + "\n### Planning Notes\n\n" + notes + "\n"
        updated_content = content.replace(task_content, updated_task)
    else:
        # Update existing Planning Notes section
        notes_section = notes_match.group(0)
        updated_notes = "### Planning Notes\n\n" + notes + "\n"
        updated_task = task_content.replace(notes_section, updated_notes)
        updated_content = content.replace(task_content, updated_task)
    
    # Write back to file
    with open(PLAN_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)
    
    if ctx:
        ctx.info(f"Updated planning notes for task: {task_title}")
    
    return f"Updated planning notes for task '{task_title}'."

@mcp.resource("plan://{task_title}")
def get_plan_resource(task_title: str = None) -> str:
    """
    Get the plan contents as a resource.
    
    Args:
        task_title: Specific task to retrieve (retrieves the entire plan if not specified)
    
    Returns:
        The current plan contents
    """
    ensure_plan_file_exists()
    
    with open(PLAN_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    
    if task_title and task_title != "all":
        # Find the specific task section
        task_pattern = re.compile(rf'## {re.escape(task_title)}\n(.+?)(?=\n## |$)', re.DOTALL)
        task_match = task_pattern.search(content)
        
        if not task_match:
            return f"Task '{task_title}' not found in the plan."
        
        return f"# Task: {task_title}\n\n" + task_match.group(0)
    else:
        return content

@mcp.tool()
def check_task_completion(task_title: str = None, ctx: Context = None) -> str:
    """
    Check if all steps in a task are marked as complete.
    
    Args:
        task_title: The task title to check (uses the latest task if not specified)
    
    Returns:
        A summary of task completion status
    """
    ensure_plan_file_exists()
    
    with open(PLAN_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    
    # If no specific task, find the most recent task section
    if not task_title:
        task_sections = re.findall(r'## (.+?)\n', content)
        if not task_sections:
            return "No tasks found in the plan."
        task_title = task_sections[-1]
    
    # Find the task section
    task_pattern = re.compile(rf'## {re.escape(task_title)}\n(.+?)(?=\n## |$)', re.DOTALL)
    task_match = task_pattern.search(content)
    
    if not task_match:
        return f"Task '{task_title}' not found in the plan."
    
    task_content = task_match.group(0)
    
    # Count total steps and completed steps
    incomplete_steps = re.findall(r'\[ \] (.+?)(?=\n|$)', task_content)
    completed_steps = re.findall(r'\[✅\] (.+?)(?=\n|$)', task_content)
    
    total_steps = len(incomplete_steps) + len(completed_steps)
    
    if total_steps == 0:
        return f"No steps found for task '{task_title}'."
    
    completion_percentage = (len(completed_steps) / total_steps) * 100
    
    result = f"Task '{task_title}' completion status:\n"
    result += f"- {len(completed_steps)} of {total_steps} steps completed ({completion_percentage:.1f}%)\n"
    
    if incomplete_steps:
        result += "\nRemaining steps:\n"
        for step in incomplete_steps:
            result += f"- {step}\n"
    
    if completed_steps and len(completed_steps) == total_steps:
        result += "\n🎉 All steps completed!"
    
    if ctx:
        ctx.info(f"Checked completion status for task: {task_title}")
    
    return result

# Run the server
if __name__ == "__main__":
    mcp.run()