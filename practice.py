class hello:
    global_count = 0
    def __init__(self, comment, count):
        self.comment = comment
        self.count = count

    def print_hello(self):
        if self.count == 0:
            return
        hello.global_count += 1
        print(self.comment, hello.global_count)
        self.count -= 1
        self.print_hello()
# hello("hi", 10).print_hello()

# text = "https://nomadcoder.co/name/code?32joifj903sdf"
# split_text = text.split("/")
# print(split_text[2])

list = ["a", "b", "c", "d"]
del list[1:]
print(list)