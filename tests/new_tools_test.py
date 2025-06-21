import winup
from winup import ui, component
from winup.tools import camera, filesystem
import os
import sys

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@component
def App():
    """A component to test the new Camera and Filesystem tools."""
    
    log_output = ui.Textarea(props={"read-only": True, "height": "200px"})

    def log(message):
        """Helper to print to console and the UI log."""
        print(message)
        current_text = log_output.toPlainText()
        log_output.setPlainText(current_text + message + "\n")

    def test_camera():
        log("--- Testing Camera ---")
        try:
            cam = camera.Camera()
            pixmap = cam.capture_frame()
            if pixmap:
                capture_path = "test_capture.png"
                pixmap.save(capture_path)
                log(f"✅ Camera frame captured and saved to '{capture_path}'.")
            else:
                log("❌ ERROR: Failed to capture frame from camera.")
            cam.release()
        except Exception as e:
            log(f"❌ ERROR: Camera test failed: {e}")

    def test_filesystem():
        log("\n--- Testing Filesystem ---")
        test_dir = "temp_test_dir"
        test_file = os.path.join(test_dir, "test.json")
        try:
            # Create directory
            filesystem.create_dir(test_dir)
            log(f"✅ Created directory: '{test_dir}'")
            
            # Write JSON
            data = {"name": "WinUp", "version": "1.0"}
            filesystem.write_json(test_file, data)
            log(f"✅ Wrote JSON to: '{test_file}'")

            # Read JSON
            read_data = filesystem.read_json(test_file)
            if read_data == data:
                log("✅ JSON read back successfully.")
            else:
                log(f"❌ ERROR: JSON data mismatch. Got {read_data}")

        except Exception as e:
            log(f"❌ ERROR: Filesystem test failed: {e}")
        finally:
            # Cleanup
            if filesystem.exists(test_dir):
                filesystem.remove(test_dir)
                log(f"✅ Cleaned up directory: '{test_dir}'")

    return ui.Column(props={"spacing": 15, "margin": "20px"}, children=[
        ui.Label("New Tools Test", props={"font-size": "20px", "font-weight": "bold"}),
        log_output,
        ui.Row(props={"spacing": 10}, children=[
            ui.Button("Test Camera", on_click=test_camera),
            ui.Button("Test Filesystem", on_click=test_filesystem)
        ])
    ])

if __name__ == "__main__":
    winup.run(
        main_component_path="tests.new_tools_test:App",
        title="Camera & Filesystem Test",
        width=600,
        height=400,
        dev=True
    ) 