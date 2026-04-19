class CalculatorTool:
    def run(self, expression):
        try:
            result = eval(expression)
            return {"results": [{"content": str(result)}]}
        except Exception as e:
            return {"results": [{"content": f"Error: {str(e)}"}]}
