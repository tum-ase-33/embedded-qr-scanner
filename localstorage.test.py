from localstorage import LocalStorage

store = LocalStorage()

print("#1: Should return empty Array List")
print(str(store.getAll()))

print("#2: Create Element: ")
store.store("attendance", "token343")
store.store("attendance", "token3434")
print('Should return two elements with ["attendance", "token343", 1234567]')
print(str(store.getAll()))

print("#3: Clear")
print("Should return empty list")
store.clear()
print(str(store.getAll()))