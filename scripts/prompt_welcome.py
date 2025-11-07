import argparse
import webbrowser
import sys

GITHUB_REPO = "https://github.com/spyrosze/mcp-openfoodtox"  # Update with your repo
DISCUSSIONS_URL = f"{GITHUB_REPO}/discussions/new?category=feedback"

def prompt_feedback():
    print("\n" + "="*60)
    print("🎉 Setup complete!\nYou can now install in Claude desktop by running 'make claude'.\nThank you for using mcp-openfoodtox!")
    print("="*60)
    print("\nIf you find this useful, please consider:")
    print("  ⭐ Starring the repo: https://github.com/spyrosze/mcp-openfoodtox")
    print("  💬 Leaving feedback: https://github.com/spyrosze/mcp-openfoodtox/discussions")
    print("  👾 Contributors welcome: https://github.com/spyrosze/mcp-openfoodtox/discussions")
    print("\nWould you like to open the feedback page now? (y/n): ", end="")
    
    response = input().strip().lower()
    if response in ['y', 'yes']:
        webbrowser.open(DISCUSSIONS_URL)
        print("Opened feedback page in your browser!")
    print()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prompt for feedback after setup")
    parser.add_argument("--skip", action="store_true", help="Skip the feedback prompt")
    args = parser.parse_args()
    
    if not args.skip:
        prompt_feedback()