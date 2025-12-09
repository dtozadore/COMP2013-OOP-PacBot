from Graphics.window import Window

def main():
    window = Window()
    
    while window.running:
        window.handleEvents()
        window.update()
        window.draw()

if __name__ == "__main__":
    main()