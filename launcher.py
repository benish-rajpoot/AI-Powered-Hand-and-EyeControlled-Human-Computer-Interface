"""
AI-Powered Hand and Eye Controlled HCI - Launcher

Provides flexible ways to launch the application:
- With settings GUI
- Direct start
- Using Application class
"""

import sys
import argparse
from pathlib import Path

# Add directories to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))
sys.path.insert(0, str(project_root / "gui"))


def main():
    """Main launcher function."""
    parser = argparse.ArgumentParser(
        description="AI-Powered Hand and Eye Controlled HCI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python launcher.py              Launch with settings GUI
  python launcher.py --no-gui     Skip GUI, start directly
  python launcher.py --settings-only  Open settings only
  python launcher.py --legacy     Use legacy main.py
        """
    )
    parser.add_argument(
        "--no-gui",
        action="store_true",
        help="Skip settings GUI and start directly"
    )
    parser.add_argument(
        "--settings-only",
        action="store_true",
        help="Open settings GUI only, don't start application"
    )
    parser.add_argument(
        "--legacy",
        action="store_true",
        help="Use legacy main.py instead of Application class"
    )
    args = parser.parse_args()
    
    # Show settings GUI unless --no-gui flag is set
    if not args.no_gui:
        print("=" * 50)
        print("AI-Powered Hand & Eye Controlled HCI")
        print("=" * 50)
        print("\nOpening Settings GUI...")
        
        try:
            from settings_gui import run_settings
            settings = run_settings()
            print(f"\nSettings configured.")
        except ImportError as e:
            print(f"Warning: Could not load GUI: {e}")
            print("Starting without GUI...")
        except Exception as e:
            print(f"GUI closed.")
    
    # Run main application unless --settings-only flag is set
    if not args.settings_only:
        print("\n" + "=" * 50)
        print("Starting Application...")
        print("=" * 50)
        
        try:
            if args.legacy:
                # Use legacy main.py
                from main import main as run_app
                run_app()
            else:
                # Use new Application class
                from app import HCIApplication
                app = HCIApplication()
                app.run()
                
        except KeyboardInterrupt:
            print("\nApplication interrupted by user")
        except Exception as e:
            print(f"Error running application: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
