import cx_Freeze

executables = [cx_Freeze.Executable("fruit.py")]

cx_Freeze.setup(
    name = "Fruit Frontier!",
    options = {"build_exe": {"packages":["pygame"],
                             "include_files":["apple.PNG","background.ogg","banana2.png","coconut.png","cuanimation.png","dead.wav","dead_banana.png","gameover.png","grapes.png","highscore.txt","laser2.wav","logo.png","object.wav","orange2.png","pineapple.png","pom.png","rainbow.png","shield.png","spike.png"]}},
    executables = executables)
