from src.window import Window

def main():
    window = Window(current_scene="menu")
    
    while window.running:
        window.handle_events()
        window.update()
        window.draw()

if __name__ == "__main__":
    main()