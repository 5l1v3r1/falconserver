class Compile:
    async def on_post(self, req, res, lang):
        with open("test.py", "w+") as f:
            f.write(req.context["code"])