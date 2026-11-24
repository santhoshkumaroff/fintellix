# OOP Basics (JD: "OOP basics")

### Q1. What is OOP? What are its 4 pillars?
**Answer:** Object-Oriented Programming organises code around **objects** (data + behaviour). Its pillars:
1. **Encapsulation:** bundle data and methods together, and hide internals.
2. **Abstraction:** expose only what's needed, behind a simple interface.
3. **Inheritance:** a child class reuses and extends a parent class.
4. **Polymorphism:** the same method name behaves differently for different classes.
- **Example 1:** A `Loan` class holds balance and DPD (data) plus `is_npa()` (behaviour).
- **Example 2:** An `LLMClient` hides API keys and HTTP retries. Callers just call `.ask(prompt)`.

### Q2. What is a class and an object?
**Answer:** A class is the blueprint. An object (instance) is a concrete thing built from it.
```python
class Loan:
    def __init__(self, loan_id: str, balance: float, dpd: int):
        self.loan_id = loan_id
        self.balance = balance
        self.dpd = dpd

    def is_npa(self) -> bool:
        return self.dpd > 90

l1 = Loan("L001", 500000, 120)   # object
l1.is_npa()                       # True
```
- **Example 2:** `Customer` class → objects `Customer("Asha")` and `Customer("Ravi")`.

### Q3. What is `__init__`? What is `self`?
**Answer:** `__init__` is the initialiser that runs when you create an object, to set its attributes. `self` is the reference to the current instance. Python passes it automatically.
- **Example 1:** `Loan("L001", 5e5, 10)` calls `__init__(self, "L001", 5e5, 10)`.
- **Example 2:** Inside a method, `self.balance` reads this loan's balance, not another loan's.

### Q4. Encapsulation in Python – private variables?
**Answer:** Python has no true private members. By convention, `_x` means "internal" and `__x` triggers name mangling (`_ClassName__x`). Use `@property` for controlled access.
```python
class Account:
    def __init__(self, balance):
        self._balance = balance
    @property
    def balance(self): return self._balance
    def withdraw(self, amt):
        if amt > self._balance: raise ValueError("Insufficient funds")
        self._balance -= amt
```
- **Example 2:** The API key is stored as `self._api_key` and never printed in `__repr__`.

### Q5. What is inheritance? Example?
**Answer:** A child class gets the parent's attributes and methods and can override or extend them. Call `super()` to reuse the parent's code.
```python
class Report:
    def __init__(self, name): self.name = name
    def validate(self, df): return df.notna().all().all()
    def export(self, df): raise NotImplementedError

class RBIReport(Report):
    def export(self, df): df.to_csv(f"{self.name}.csv", index=False)

class CBUAEReport(Report):
    def export(self, df): df.to_xml(f"{self.name}.xml")   # needs lxml installed
```
- **Example 2:** `HomeLoan(Loan)` adds a `collateral_value` attribute and an LTV calculation.

### Q6. What is polymorphism?
**Answer:** Different classes provide the same method name, and calling code treats them uniformly.
- **Example 1:** `for r in [RBIReport("npa"), CBUAEReport("liq")]: r.export(df)` calls each class's own export.
- **Example 2:** `len()` works on str, list and dict. Each type implements `__len__`.

### Q7. What is abstraction / abstract base class?
**Answer:** Define an interface that subclasses **must** implement, using `abc.ABC` and `@abstractmethod`. You can't instantiate the abstract class.
```python
from abc import ABC, abstractmethod
class LLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str: ...

class ClaudeProvider(LLMProvider):
    def generate(self, prompt): ...   # calls Anthropic API
class LocalProvider(LLMProvider):
    def generate(self, prompt): ...   # calls a local model
```
- **Example 2:** A `DataSource` interface with `read()`, implemented by `CSVSource`, `SQLSource` and `ExcelSource`.

### Q8. Class variable vs instance variable?
**Answer:** A class variable is shared by all instances. An instance variable is per object.
```python
class Loan:
    npa_threshold = 90            # class variable (same for all)
    def __init__(self, dpd): self.dpd = dpd   # instance variable
    def is_npa(self): return self.dpd > Loan.npa_threshold
```
- **Example 2:** A counter of how many `Loan` objects were created: `Loan.count += 1` inside `__init__`.

### Q9. Instance method vs `@classmethod` vs `@staticmethod`?
- **Instance method:** takes `self` and works on one object. Example: `loan.is_npa()`.
- **@classmethod:** takes `cls`. Often used as an alternative constructor. Example: `Loan.from_dict(row)`.
- **@staticmethod:** takes neither. It's a utility that logically belongs to the class. Example: `Loan.validate_id("L001")`.
```python
class Loan:
    def __init__(self, loan_id, dpd): self.loan_id, self.dpd = loan_id, dpd
    @classmethod
    def from_dict(cls, d): return cls(d["id"], int(d["dpd"]))
    @staticmethod
    def validate_id(x): return x.startswith("L") and x[1:].isdigit()
```

### Q10. What are dunder (magic) methods?
**Answer:** Special methods such as `__init__`, `__repr__`, `__str__`, `__len__`, `__eq__`, `__lt__` and `__add__` that hook into Python syntax.
- **Example 1:** `__repr__` returns `Loan(L001, bal=500000)`, which makes debugging logs readable.
- **Example 2:** `__lt__` compares loans by balance so `sorted(loans)` works.

### Q11. What are dataclasses?
**Answer:** `@dataclass` auto-generates `__init__`, `__repr__` and `__eq__` for classes that mainly hold data.
```python
from dataclasses import dataclass
@dataclass
class ValidationResult:
    rule_id: str
    passed: bool
    failed_rows: int = 0
```
- **Example 2:** Storing each GenAI evaluation result: `EvalCase(question, expected, actual, score)`.

### Q12. Composition vs inheritance?
**Answer:** Inheritance models "is-a" (a HomeLoan **is a** Loan). Composition models "has-a" (a RAGPipeline **has a** Retriever and **has an** LLM). Prefer composition for flexibility.
- **Example 1:** `class RAGPipeline: def __init__(self, retriever, llm): ...` lets you swap FAISS for Chroma without changing the pipeline.
- **Example 2:** A `ReportGenerator` that has a `Validator` and an `Exporter`.

### Q13. What is multiple inheritance and MRO?
**Answer:** A class can inherit from several parents. Python resolves method lookup with the **Method Resolution Order** (C3 linearisation). See it with `Class.__mro__`.
- **Example:** `class AuditedReport(LoggingMixin, Report)`: the mixin adds logging to any report.

### Q14. When would you NOT use OOP?
**Answer:** For small scripts or pure data transformations, plain functions and pandas pipelines are simpler. Use classes when there's state plus behaviour, or several interchangeable implementations.
- **Example 1:** A 30-line script that renames columns doesn't need classes.
- **Example 2:** A multi-provider LLM client with retries, logging and cost tracking benefits from a class.
