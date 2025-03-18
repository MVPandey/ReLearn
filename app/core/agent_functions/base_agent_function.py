from abc import abstractmethod


class BaseAgentFunction:

    @abstractmethod
    def add_mappings(self):
        """
        This must be implemented by the subclass. It maps the function name to the function.

        E.g.

        def add_mappings(self):
            return {
                "function_name": self.function,
            }
        """
        pass
