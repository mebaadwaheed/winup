# winup/web/script_manager.py

class ScriptManager:
    """
    A singleton class to collect JavaScript snippets for lifecycle hooks
    from all components in a render tree.
    """
    def __init__(self):
        self.reset()

    def reset(self):
        """Clears all scripts. Called at the start of each web request."""
        self._mount_scripts = {}
        self._unmount_scripts = {}

    def add_mount_script(self, component_id: str, script: str):
        """Adds an on_mount script for a given component ID."""
        self._mount_scripts[component_id] = script

    def add_unmount_script(self, component_id: str, script: str):
        """Adds an on_unmount script for a given component ID."""
        self._unmount_scripts[component_id] = script

    def generate_script(self) -> str:
        """
        Generates the final JavaScript code to be injected into the HTML.
        This code finds the components by ID and executes their hooks.
        It uses a MutationObserver to detect when elements are removed
        from the DOM to fire on_unmount events.
        """
        if not self._mount_scripts and not self._unmount_scripts:
            return ""

        mount_js = "{\n" + ",\n".join([f'  "{cid}": (element) => {{ {script} }}' for cid, script in self._mount_scripts.items()]) + "\n}"
        unmount_js = "{\n" + ",\n".join([f'  "{cid}": (element) => {{ {script} }}' for cid, script in self._unmount_scripts.items()]) + "\n}"

        return f"""
document.addEventListener('DOMContentLoaded', () => {{
    const mount_hooks = {mount_js};
    const unmount_hooks = {unmount_js};

    // --- Run initial mount hooks ---
    for (const id in mount_hooks) {{
        const el = document.getElementById(id);
        if (el) {{
            try {{
                mount_hooks[id](el);
            }} catch (e) {{
                console.error(`Error in on_mount for component #${{id}}:`, e);
            }}
        }}
    }}

    // --- Set up unmount observer ---
    const observer = new MutationObserver((mutationsList) => {{
        for (const mutation of mutationsList) {{
            if (mutation.type === 'childList') {{
                mutation.removedNodes.forEach(node => {{
                    const checkNodeAndChildren = (n) => {{
                        if (n.id && unmount_hooks[n.id]) {{
                            try {{
                                unmount_hooks[n.id](n);
                            }} catch (e) {{
                                console.error(`Error in on_unmount for component #${{n.id}}:`, e);
                            }}
                            delete unmount_hooks[n.id]; // Run only once
                        }}
                        if (n.querySelectorAll) {{
                            Object.keys(unmount_hooks).forEach(id => {{
                                const el = n.querySelector('#' + id);
                                if (el) {{
                                     try {{
                                        unmount_hooks[id](el);
                                    }} catch (e) {{
                                        console.error(`Error in on_unmount for component #${{id}}:`, e);
                                    }}
                                    delete unmount_hooks[id];
                                }}
                            }});
                        }}
                    }};
                    checkNodeAndChildren(node);
                }});
            }}
        }}
    }});

    // Start observing the body for added/removed nodes
    observer.observe(document.body, {{ childList: true, subtree: true }});
}});
"""

# Singleton instance for global access
script_manager = ScriptManager() 