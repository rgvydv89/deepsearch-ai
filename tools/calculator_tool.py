class CalculatorTool:
    name = "calculator"
    description = "Perform mathematical calculations"
    input_schema = {"expression": "string"}

    def execute(self, expression):
        try:
            result = eval(expression)

            return [
                {
                    "title": "Calculation Result",
                    "url": "local://calculator",
                    "content": str(result)
                }
            ]
        except Exception as e:
            return [
                {
                    "title": "Error",
                    "url": "local://calculator-error",
                    "content": str(e)
                }
            ]