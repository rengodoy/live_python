class teste(object):
    pass
    
    def __init__(self):
         
        print('comecou')
    
    def __str__(self):
        return f'Objeto do tipo {type(self)}!'



print("iniciao do script")
a = teste()
print(type(a))
print(a)

