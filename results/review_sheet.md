# Bảng chấm và đối chiếu — Day 06

**Trần Văn Quang · 2A202604032 · L3B**

**Xác nhận:** Trần Văn Quang đã đọc trực tiếp, duyệt thủ công các mẫu đánh giá và phê duyệt kết quả trong báo cáo. [Bản ghi phê duyệt](approval.json)

Bảng này tập hợp toàn bộ 30 nhãn coherence, 15 nhãn grounding và 45 bản ghi metadata đã lưu. Coherence và grounding được ChatGPT/Codex chấm từng mẫu theo thang 0–2 của GUIDE rồi rà lại với nguồn; metadata được đối chiếu bằng script. Trần Văn Quang đã trực tiếp đọc các mẫu, duyệt thủ công và xác nhận giữ nguyên kết quả. Bản ghi phê duyệt lưu xác nhận của tác giả; thông tin tạo nhãn ban đầu vẫn được giữ trong hồ sơ audit.

## Tổng hợp

| Cấu hình | Coherence /2 (10 mẫu) | Grounding /2 (5 câu) | Metadata đủ và đúng | Filter dev | Filter test |
|---|---:|---:|---:|---:|---:|
| A | 1.00 | 2.00 | 15/15 | 2/3 | 0/1 |
| B | 1.80 | 2.00 | 15/15 | 2/3 | 1/1 |
| C | 1.80 | 2.00 | 15/15 | 3/3 | 1/1 |

## Coherence — 30 mẫu

0: thiếu ý hoặc chủ thể đến mức không hiểu; 1: hiểu một phần nhưng thiếu ngữ cảnh; 2: giữ trọn ý và tự hiểu được. Cùng 10 vị trí nguồn được dùng cho cả ba cấu hình.

| Mẫu | Cấu hình | Đơn vị nguồn | Điểm /2 | Lý do |
|---|---|---|---:|---|
| s01 | A | classes-001 | 1 | Đoạn đầu giải thích class rõ, nhưng câu so sánh với ngôn ngữ khác bị cắt ở cuối chunk. |
| s02 | A | classes-007 | 1 | Ví dụ Dog còn đọc được; cảnh báo về dữ liệu dùng chung bị cắt giữa từ ở cuối. |
| s03 | A | controlflow-001 | 1 | Giữ điều kiện if nhưng cắt phần ví dụ ngay trước kết quả và giải thích. |
| s04 | A | controlflow-007 | 1 | Nhận định về None còn đọc được, câu chỉ cách xem giá trị bị cắt. |
| s05 | A | controlflow-014 | 1 | Giữ quy tắc thụt lề; câu quy định độ dài dòng dừng giữa ý. |
| s06 | A | datastructures-006 | 1 | Ví dụ tập hợp bị ngắt trong phần giải thích phép toán và kết quả. |
| s07 | A | errors-004 | 1 | Ví dụ xử lý lỗi đầy đủ, phần giải thích raise tiếp theo bị cắt giữa từ. |
| s08 | A | inputoutput-002 | 1 | Ví dụ repr bị ngắt trước khi hoàn tất chú thích và lời gọi cuối. |
| s09 | A | modules-002 | 1 | Đoạn namespace đủ ý; đoạn giới thiệu import ngay sau bị cắt giữa câu. |
| s10 | A | modules-008 | 1 | Giải thích shadowing được giữ nhưng danh sách __all__ bị cắt giữa chuỗi. |
| s01 | B | classes-001 | 2 | Giữ trọn đoạn định nghĩa class, instance, thuộc tính và phương thức. |
| s02 | B | classes-007 | 2 | Ví dụ phân biệt class/instance cùng cảnh báo mutable class variable và ví dụ Dog đều đầy đủ. |
| s03 | B | controlflow-001 | 2 | Ví dụ if/elif/else có đầu vào, kết quả và giải thích các nhánh. |
| s04 | B | controlflow-007 | 1 | Giải thích None đủ, nhưng câu dẫn tới ví dụ trả danh sách ở cuối không kèm ví dụ. |
| s05 | B | controlflow-014 | 2 | Các quy tắc PEP 8 về thụt lề, độ dài dòng, khoảng trắng đều kết thúc đầy đủ. |
| s06 | B | datastructures-006 | 1 | Ví dụ các phép toán set đầy đủ, câu mở sang set comprehension thiếu ví dụ tiếp theo. |
| s07 | B | errors-004 | 2 | Giữ ví dụ lỗi được bắt trong hàm con và ví dụ raise NameError có kết quả. |
| s08 | B | inputoutput-002 | 2 | Các ví dụ str/repr có cả đầu vào và kết quả; đủ hiểu khác biệt được minh họa. |
| s09 | B | modules-002 | 2 | Giải thích namespace, import và from-import có ngữ cảnh cùng ví dụ. |
| s10 | B | modules-008 | 2 | Giải thích shadowing và mã __all__/reverse được giữ trọn. |
| s01 | C | classes-001 | 2 | Giữ trọn đoạn định nghĩa class, instance, thuộc tính và phương thức. C dùng cùng chunk với B. |
| s02 | C | classes-007 | 2 | Ví dụ phân biệt class/instance cùng cảnh báo mutable class variable và ví dụ Dog đều đầy đủ. C dùng cùng chunk với B. |
| s03 | C | controlflow-001 | 2 | Ví dụ if/elif/else có đầu vào, kết quả và giải thích các nhánh. C dùng cùng chunk với B. |
| s04 | C | controlflow-007 | 1 | Giải thích None đủ, nhưng câu dẫn tới ví dụ trả danh sách ở cuối không kèm ví dụ. C dùng cùng chunk với B. |
| s05 | C | controlflow-014 | 2 | Các quy tắc PEP 8 về thụt lề, độ dài dòng, khoảng trắng đều kết thúc đầy đủ. C dùng cùng chunk với B. |
| s06 | C | datastructures-006 | 1 | Ví dụ các phép toán set đầy đủ, câu mở sang set comprehension thiếu ví dụ tiếp theo. C dùng cùng chunk với B. |
| s07 | C | errors-004 | 2 | Giữ ví dụ lỗi được bắt trong hàm con và ví dụ raise NameError có kết quả. C dùng cùng chunk với B. |
| s08 | C | inputoutput-002 | 2 | Các ví dụ str/repr có cả đầu vào và kết quả; đủ hiểu khác biệt được minh họa. C dùng cùng chunk với B. |
| s09 | C | modules-002 | 2 | Giải thích namespace, import và from-import có ngữ cảnh cùng ví dụ. C dùng cùng chunk với B. |
| s10 | C | modules-008 | 2 | Giải thích shadowing và mã __all__/reverse được giữ trọn. C dùng cùng chunk với B. |

### Nội dung các chunk đã chấm

<details>
<summary>s01 — A — classes-001 — 1/2</summary>

[Trang nguồn](https://docs.python.org/3.13/tutorial/classes.html); vị trí ký tự 0–500 trong đơn vị.

<pre>9. Classes

Classes provide a means of bundling data and functionality together.  Creating
a new class creates a new type of object, allowing new instances of that
type to be made.  Each class instance can have attributes attached to it for
maintaining its state.  Class instances can also have methods (defined by its
class) for modifying its state.

Compared with other programming languages, Python’s class mechanism adds classes
with a minimum of new syntax and semantics.  It is a mixture of the</pre>

</details>

<details>
<summary>s02 — A — classes-007 — 1/2</summary>

[Trang nguồn](https://docs.python.org/3.13/tutorial/classes.html); vị trí ký tự 0–500 trong đơn vị.

<pre>class Dog:

    kind = &#x27;canine&#x27;         # class variable shared by all instances

    def __init__(self, name):
        self.name = name    # instance variable unique to each instance

&gt;&gt;&gt; d = Dog(&#x27;Fido&#x27;)
&gt;&gt;&gt; e = Dog(&#x27;Buddy&#x27;)
&gt;&gt;&gt; d.kind                  # shared by all dogs
&#x27;canine&#x27;
&gt;&gt;&gt; e.kind                  # shared by all dogs
&#x27;canine&#x27;
&gt;&gt;&gt; d.name                  # unique to d
&#x27;Fido&#x27;
&gt;&gt;&gt; e.name                  # unique to e
&#x27;Buddy&#x27;

As discussed in A Word About Names and Objects , shared da</pre>

</details>

<details>
<summary>s03 — A — controlflow-001 — 1/2</summary>

[Trang nguồn](https://docs.python.org/3.13/tutorial/controlflow.html); vị trí ký tự 0–500 trong đơn vị.

<pre>4. More Control Flow Tools

As well as the while statement just introduced, Python uses a few more
that we will encounter in this chapter.

4.1. if Statements

Perhaps the most well-known statement type is the if statement.  For
example:

&gt;&gt;&gt; x = int(input(&quot;Please enter an integer: &quot;))
Please enter an integer: 42
&gt;&gt;&gt; if x &lt; 0:
...     x = 0
...     print(&#x27;Negative changed to zero&#x27;)
... elif x == 0:
...     print(&#x27;Zero&#x27;)
... elif x == 1:
...     print(&#x27;Single&#x27;)
... else:
...     print(&#x27;More&#x27;)
...</pre>

</details>

<details>
<summary>s04 — A — controlflow-007 — 1/2</summary>

[Trang nguồn](https://docs.python.org/3.13/tutorial/controlflow.html); vị trí ký tự 0–500 trong đơn vị.

<pre>&gt;&gt;&gt; fib
&lt;function fib at 10042ed0&gt;
&gt;&gt;&gt; f = fib
&gt;&gt;&gt; f(100)
0 1 1 2 3 5 8 13 21 34 55 89

Coming from other languages, you might object that fib is not a function but
a procedure since it doesn’t return a value.  In fact, even functions without a return statement do return a value, albeit a rather boring one.  This
value is called None (it’s a built-in name).  Writing the value None is
normally suppressed by the interpreter if it would be the only value written.
You can see it if you really want t</pre>

</details>

<details>
<summary>s05 — A — controlflow-014 — 1/2</summary>

[Trang nguồn](https://docs.python.org/3.13/tutorial/controlflow.html); vị trí ký tự 0–500 trong đơn vị.

<pre>For Python, PEP 8 has emerged as the style guide that most projects adhere to;
it promotes a very readable and eye-pleasing coding style.  Every Python
developer should read it at some point; here are the most important points
extracted for you:

Use 4-space indentation, and no tabs. 4 spaces are a good compromise between small indentation (allows greater
nesting depth) and large indentation (easier to read).  Tabs introduce
confusion, and are best left out.

Wrap lines so that they don’t exceed</pre>

</details>

<details>
<summary>s06 — A — datastructures-006 — 1/2</summary>

[Trang nguồn](https://docs.python.org/3.13/tutorial/datastructures.html); vị trí ký tự 0–500 trong đơn vị.

<pre>Here is a brief demonstration:

&gt;&gt;&gt; basket = {&#x27;apple&#x27;, &#x27;orange&#x27;, &#x27;apple&#x27;, &#x27;pear&#x27;, &#x27;orange&#x27;, &#x27;banana&#x27;}
&gt;&gt;&gt; print(basket)                      # show that duplicates have been removed
{&#x27;orange&#x27;, &#x27;banana&#x27;, &#x27;pear&#x27;, &#x27;apple&#x27;}
&gt;&gt;&gt; &#x27;orange&#x27; in basket                 # fast membership testing
True
&gt;&gt;&gt; &#x27;crabgrass&#x27; in basket
False

&gt;&gt;&gt; # Demonstrate set operations on unique letters from two words
&gt;&gt;&gt;
&gt;&gt;&gt; a = set(&#x27;abracadabra&#x27;)
&gt;&gt;&gt; b = set(&#x27;alacazam&#x27;)
&gt;&gt;&gt; a                                  # unique letters </pre>

</details>

<details>
<summary>s07 — A — errors-004 — 1/2</summary>

[Trang nguồn](https://docs.python.org/3.13/tutorial/errors.html); vị trí ký tự 0–500 trong đơn vị.

<pre>Exception handlers do not handle only exceptions that occur immediately in the try clause , but also those that occur inside functions that are called (even
indirectly) in the try clause . For example:

&gt;&gt;&gt; def this_fails():
...     x = 1/0
...
&gt;&gt;&gt; try:
...     this_fails()
... except ZeroDivisionError as err:
...     print(&#x27;Handling run-time error:&#x27;, err)
...
Handling run-time error: division by zero

8.4. Raising Exceptions

The raise statement allows the programmer to force a specified
except</pre>

</details>

<details>
<summary>s08 — A — inputoutput-002 — 1/2</summary>

[Trang nguồn](https://docs.python.org/3.13/tutorial/inputoutput.html); vị trí ký tự 0–500 trong đơn vị.

<pre>Some examples:

&gt;&gt;&gt; s = &#x27;Hello, world.&#x27;
&gt;&gt;&gt; str(s)
&#x27;Hello, world.&#x27;
&gt;&gt;&gt; repr(s)
&quot;&#x27;Hello, world.&#x27;&quot;
&gt;&gt;&gt; str(1/7)
&#x27;0.14285714285714285&#x27;
&gt;&gt;&gt; x = 10 * 3.25
&gt;&gt;&gt; y = 200 * 200
&gt;&gt;&gt; s = &#x27;The value of x is &#x27; + repr(x) + &#x27;, and y is &#x27; + repr(y) + &#x27;...&#x27;
&gt;&gt;&gt; print(s)
The value of x is 32.5, and y is 40000...
&gt;&gt;&gt; # The repr() of a string adds string quotes and backslashes:
&gt;&gt;&gt; hello = &#x27;hello, world\n&#x27;
&gt;&gt;&gt; hellos = repr(hello)
&gt;&gt;&gt; print(hellos)
&#x27;hello, world\n&#x27;
&gt;&gt;&gt; # The argument to repr() may be any Python obj</pre>

</details>

<details>
<summary>s09 — A — modules-002 — 1/2</summary>

[Trang nguồn](https://docs.python.org/3.13/tutorial/modules.html); vị trí ký tự 0–500 trong đơn vị.

<pre>Each module has its own private namespace, which is used as the global namespace
by all functions defined in the module. Thus, the author of a module can
use global variables in the module without worrying about accidental clashes
with a user’s global variables. On the other hand, if you know what you are
doing you can touch a module’s global variables with the same notation used to
refer to its functions, modname.itemname .

Modules can import other modules.  It is customary but not required to</pre>

</details>

<details>
<summary>s10 — A — modules-008 — 1/2</summary>

[Trang nguồn](https://docs.python.org/3.13/tutorial/modules.html); vị trí ký tự 0–500 trong đơn vị.

<pre>Be aware that submodules might become shadowed by locally defined names. For
example, if you added a reverse function to the sound/effects/__init__.py file, the from sound.effects import * would only import the two submodules echo and surround , but not the reverse submodule, because it is shadowed by the locally defined reverse function:

__all__ = [
    &quot;echo&quot;,      # refers to the &#x27;echo.py&#x27; file
    &quot;surround&quot;,  # refers to the &#x27;surround.py&#x27; file
    &quot;reverse&quot;,   # !!! refers to the &#x27;reverse&#x27;</pre>

</details>

<details>
<summary>s01 — B — classes-001 — 2/2</summary>

[Trang nguồn](https://docs.python.org/3.13/tutorial/classes.html); vị trí ký tự 0–350 trong đơn vị.

<pre>9. Classes

Classes provide a means of bundling data and functionality together.  Creating
a new class creates a new type of object, allowing new instances of that
type to be made.  Each class instance can have attributes attached to it for
maintaining its state.  Class instances can also have methods (defined by its
class) for modifying its state.</pre>

</details>

<details>
<summary>s02 — B — classes-007 — 2/2</summary>

[Trang nguồn](https://docs.python.org/3.13/tutorial/classes.html); vị trí ký tự 0–951 trong đơn vị.

<pre>class Dog:

    kind = &#x27;canine&#x27;         # class variable shared by all instances

    def __init__(self, name):
        self.name = name    # instance variable unique to each instance

&gt;&gt;&gt; d = Dog(&#x27;Fido&#x27;)
&gt;&gt;&gt; e = Dog(&#x27;Buddy&#x27;)
&gt;&gt;&gt; d.kind                  # shared by all dogs
&#x27;canine&#x27;
&gt;&gt;&gt; e.kind                  # shared by all dogs
&#x27;canine&#x27;
&gt;&gt;&gt; d.name                  # unique to d
&#x27;Fido&#x27;
&gt;&gt;&gt; e.name                  # unique to e
&#x27;Buddy&#x27;

As discussed in A Word About Names and Objects , shared data can have possibly surprising
effects involving mutable objects such as lists and dictionaries.
For example, the tricks list in the following code should not be used as a
class variable because just a single list would be shared by all Dog instances:

class Dog:

    tricks = []             # mistaken use of a class variable

    def __init__(self, name):
        self.name = name

    def add_trick(self, trick):
        self.tricks.append(trick)</pre>

</details>

<details>
<summary>s03 — B — controlflow-001 — 2/2</summary>

[Trang nguồn](https://docs.python.org/3.13/tutorial/controlflow.html); vị trí ký tự 0–986 trong đơn vị.

<pre>4. More Control Flow Tools

As well as the while statement just introduced, Python uses a few more
that we will encounter in this chapter.

4.1. if Statements

Perhaps the most well-known statement type is the if statement.  For
example:

&gt;&gt;&gt; x = int(input(&quot;Please enter an integer: &quot;))
Please enter an integer: 42
&gt;&gt;&gt; if x &lt; 0:
...     x = 0
...     print(&#x27;Negative changed to zero&#x27;)
... elif x == 0:
...     print(&#x27;Zero&#x27;)
... elif x == 1:
...     print(&#x27;Single&#x27;)
... else:
...     print(&#x27;More&#x27;)
...
More

There can be zero or more elif parts, and the else part is
optional.  The keyword ‘ elif ’ is short for ‘else if’, and is useful
to avoid excessive indentation.  An if … elif … elif … sequence is a substitute for the switch or case statements found in other languages.

If you’re comparing the same value to several constants, or checking for specific types or
attributes, you may also find the match statement useful. For more
details see match Statements .

4.2. for Statements</pre>

</details>

<details>
<summary>s04 — B — controlflow-007 — 1/2</summary>

[Trang nguồn](https://docs.python.org/3.13/tutorial/controlflow.html); vị trí ký tự 0–670 trong đơn vị.

<pre>&gt;&gt;&gt; fib
&lt;function fib at 10042ed0&gt;
&gt;&gt;&gt; f = fib
&gt;&gt;&gt; f(100)
0 1 1 2 3 5 8 13 21 34 55 89

Coming from other languages, you might object that fib is not a function but
a procedure since it doesn’t return a value.  In fact, even functions without a return statement do return a value, albeit a rather boring one.  This
value is called None (it’s a built-in name).  Writing the value None is
normally suppressed by the interpreter if it would be the only value written.
You can see it if you really want to using print() :

&gt;&gt;&gt; fib(0)
&gt;&gt;&gt; print(fib(0))
None

It is simple to write a function that returns a list of the numbers of the
Fibonacci series, instead of printing it:</pre>

</details>

<details>
<summary>s05 — B — controlflow-014 — 2/2</summary>

[Trang nguồn](https://docs.python.org/3.13/tutorial/controlflow.html); vị trí ký tự 0–918 trong đơn vị.

<pre>For Python, PEP 8 has emerged as the style guide that most projects adhere to;
it promotes a very readable and eye-pleasing coding style.  Every Python
developer should read it at some point; here are the most important points
extracted for you:

Use 4-space indentation, and no tabs. 4 spaces are a good compromise between small indentation (allows greater
nesting depth) and large indentation (easier to read).  Tabs introduce
confusion, and are best left out.

Wrap lines so that they don’t exceed 79 characters. This helps users with small displays and makes it possible to have several
code files side-by-side on larger displays.

Use blank lines to separate functions and classes, and larger blocks of
code inside functions.

When possible, put comments on a line of their own.

Use docstrings.

Use spaces around operators and after commas, but not directly inside
bracketing constructs: a = f(1, 2) + g(3, 4) .</pre>

</details>

<details>
<summary>s06 — B — datastructures-006 — 1/2</summary>

[Trang nguồn](https://docs.python.org/3.13/tutorial/datastructures.html); vị trí ký tự 0–975 trong đơn vị.

<pre>Here is a brief demonstration:

&gt;&gt;&gt; basket = {&#x27;apple&#x27;, &#x27;orange&#x27;, &#x27;apple&#x27;, &#x27;pear&#x27;, &#x27;orange&#x27;, &#x27;banana&#x27;}
&gt;&gt;&gt; print(basket)                      # show that duplicates have been removed
{&#x27;orange&#x27;, &#x27;banana&#x27;, &#x27;pear&#x27;, &#x27;apple&#x27;}
&gt;&gt;&gt; &#x27;orange&#x27; in basket                 # fast membership testing
True
&gt;&gt;&gt; &#x27;crabgrass&#x27; in basket
False

&gt;&gt;&gt; # Demonstrate set operations on unique letters from two words
&gt;&gt;&gt;
&gt;&gt;&gt; a = set(&#x27;abracadabra&#x27;)
&gt;&gt;&gt; b = set(&#x27;alacazam&#x27;)
&gt;&gt;&gt; a                                  # unique letters in a
{&#x27;a&#x27;, &#x27;r&#x27;, &#x27;b&#x27;, &#x27;c&#x27;, &#x27;d&#x27;}
&gt;&gt;&gt; a - b                              # letters in a but not in b
{&#x27;r&#x27;, &#x27;d&#x27;, &#x27;b&#x27;}
&gt;&gt;&gt; a | b                              # letters in a or b or both
{&#x27;a&#x27;, &#x27;c&#x27;, &#x27;r&#x27;, &#x27;d&#x27;, &#x27;b&#x27;, &#x27;m&#x27;, &#x27;z&#x27;, &#x27;l&#x27;}
&gt;&gt;&gt; a &amp; b                              # letters in both a and b
{&#x27;a&#x27;, &#x27;c&#x27;}
&gt;&gt;&gt; a ^ b                              # letters in a or b but not both
{&#x27;r&#x27;, &#x27;d&#x27;, &#x27;b&#x27;, &#x27;m&#x27;, &#x27;z&#x27;, &#x27;l&#x27;}

Similarly to list comprehensions , set comprehensions
are also supported:</pre>

</details>

<details>
<summary>s07 — B — errors-004 — 2/2</summary>

[Trang nguồn](https://docs.python.org/3.13/tutorial/errors.html); vị trí ký tự 0–681 trong đơn vị.

<pre>Exception handlers do not handle only exceptions that occur immediately in the try clause , but also those that occur inside functions that are called (even
indirectly) in the try clause . For example:

&gt;&gt;&gt; def this_fails():
...     x = 1/0
...
&gt;&gt;&gt; try:
...     this_fails()
... except ZeroDivisionError as err:
...     print(&#x27;Handling run-time error:&#x27;, err)
...
Handling run-time error: division by zero

8.4. Raising Exceptions

The raise statement allows the programmer to force a specified
exception to occur. For example:

&gt;&gt;&gt; raise NameError(&#x27;HiThere&#x27;)
Traceback (most recent call last):
  File &quot;&lt;stdin&gt;&quot;, line 1, in &lt;module&gt;
    raise NameError(&#x27;HiThere&#x27;)
NameError: HiThere</pre>

</details>

<details>
<summary>s08 — B — inputoutput-002 — 2/2</summary>

[Trang nguồn](https://docs.python.org/3.13/tutorial/inputoutput.html); vị trí ký tự 0–840 trong đơn vị.

<pre>Some examples:

&gt;&gt;&gt; s = &#x27;Hello, world.&#x27;
&gt;&gt;&gt; str(s)
&#x27;Hello, world.&#x27;
&gt;&gt;&gt; repr(s)
&quot;&#x27;Hello, world.&#x27;&quot;
&gt;&gt;&gt; str(1/7)
&#x27;0.14285714285714285&#x27;
&gt;&gt;&gt; x = 10 * 3.25
&gt;&gt;&gt; y = 200 * 200
&gt;&gt;&gt; s = &#x27;The value of x is &#x27; + repr(x) + &#x27;, and y is &#x27; + repr(y) + &#x27;...&#x27;
&gt;&gt;&gt; print(s)
The value of x is 32.5, and y is 40000...
&gt;&gt;&gt; # The repr() of a string adds string quotes and backslashes:
&gt;&gt;&gt; hello = &#x27;hello, world\n&#x27;
&gt;&gt;&gt; hellos = repr(hello)
&gt;&gt;&gt; print(hellos)
&#x27;hello, world\n&#x27;
&gt;&gt;&gt; # The argument to repr() may be any Python object:
&gt;&gt;&gt; repr((x, y, (&#x27;spam&#x27;, &#x27;eggs&#x27;)))
&quot;(32.5, 40000, (&#x27;spam&#x27;, &#x27;eggs&#x27;))&quot;

The string module contains a Template class that offers
yet another way to substitute values into strings, using placeholders like $x and replacing them with values from a dictionary, but offers much less
control of the formatting.

7.1.1. Formatted String Literals</pre>

</details>

<details>
<summary>s09 — B — modules-002 — 2/2</summary>

[Trang nguồn](https://docs.python.org/3.13/tutorial/modules.html); vị trí ký tự 0–959 trong đơn vị.

<pre>Each module has its own private namespace, which is used as the global namespace
by all functions defined in the module. Thus, the author of a module can
use global variables in the module without worrying about accidental clashes
with a user’s global variables. On the other hand, if you know what you are
doing you can touch a module’s global variables with the same notation used to
refer to its functions, modname.itemname .

Modules can import other modules.  It is customary but not required to place all import statements at the beginning of a module (or script, for that
matter).  The imported module names, if placed at the top level of a module
(outside any functions or classes), are added to the module’s global namespace.

There is a variant of the import statement that imports names from a
module directly into the importing module’s namespace.  For example:

&gt;&gt;&gt; from fibo import fib, fib2
&gt;&gt;&gt; fib(500)
0 1 1 2 3 5 8 13 21 34 55 89 144 233 377</pre>

</details>

<details>
<summary>s10 — B — modules-008 — 2/2</summary>

[Trang nguồn](https://docs.python.org/3.13/tutorial/modules.html); vị trí ký tự 0–672 trong đơn vị.

<pre>Be aware that submodules might become shadowed by locally defined names. For
example, if you added a reverse function to the sound/effects/__init__.py file, the from sound.effects import * would only import the two submodules echo and surround , but not the reverse submodule, because it is shadowed by the locally defined reverse function:

__all__ = [
    &quot;echo&quot;,      # refers to the &#x27;echo.py&#x27; file
    &quot;surround&quot;,  # refers to the &#x27;surround.py&#x27; file
    &quot;reverse&quot;,   # !!! refers to the &#x27;reverse&#x27; function now !!!
]

def reverse(msg: str):  # &lt;-- this name shadows the &#x27;reverse.py&#x27; submodule
    return msg[::-1]    #     in the case of a &#x27;from sound.effects import *&#x27;</pre>

</details>

<details>
<summary>s01 — C — classes-001 — 2/2</summary>

[Trang nguồn](https://docs.python.org/3.13/tutorial/classes.html); vị trí ký tự 0–350 trong đơn vị.

<pre>9. Classes

Classes provide a means of bundling data and functionality together.  Creating
a new class creates a new type of object, allowing new instances of that
type to be made.  Each class instance can have attributes attached to it for
maintaining its state.  Class instances can also have methods (defined by its
class) for modifying its state.</pre>

</details>

<details>
<summary>s02 — C — classes-007 — 2/2</summary>

[Trang nguồn](https://docs.python.org/3.13/tutorial/classes.html); vị trí ký tự 0–951 trong đơn vị.

<pre>class Dog:

    kind = &#x27;canine&#x27;         # class variable shared by all instances

    def __init__(self, name):
        self.name = name    # instance variable unique to each instance

&gt;&gt;&gt; d = Dog(&#x27;Fido&#x27;)
&gt;&gt;&gt; e = Dog(&#x27;Buddy&#x27;)
&gt;&gt;&gt; d.kind                  # shared by all dogs
&#x27;canine&#x27;
&gt;&gt;&gt; e.kind                  # shared by all dogs
&#x27;canine&#x27;
&gt;&gt;&gt; d.name                  # unique to d
&#x27;Fido&#x27;
&gt;&gt;&gt; e.name                  # unique to e
&#x27;Buddy&#x27;

As discussed in A Word About Names and Objects , shared data can have possibly surprising
effects involving mutable objects such as lists and dictionaries.
For example, the tricks list in the following code should not be used as a
class variable because just a single list would be shared by all Dog instances:

class Dog:

    tricks = []             # mistaken use of a class variable

    def __init__(self, name):
        self.name = name

    def add_trick(self, trick):
        self.tricks.append(trick)</pre>

</details>

<details>
<summary>s03 — C — controlflow-001 — 2/2</summary>

[Trang nguồn](https://docs.python.org/3.13/tutorial/controlflow.html); vị trí ký tự 0–986 trong đơn vị.

<pre>4. More Control Flow Tools

As well as the while statement just introduced, Python uses a few more
that we will encounter in this chapter.

4.1. if Statements

Perhaps the most well-known statement type is the if statement.  For
example:

&gt;&gt;&gt; x = int(input(&quot;Please enter an integer: &quot;))
Please enter an integer: 42
&gt;&gt;&gt; if x &lt; 0:
...     x = 0
...     print(&#x27;Negative changed to zero&#x27;)
... elif x == 0:
...     print(&#x27;Zero&#x27;)
... elif x == 1:
...     print(&#x27;Single&#x27;)
... else:
...     print(&#x27;More&#x27;)
...
More

There can be zero or more elif parts, and the else part is
optional.  The keyword ‘ elif ’ is short for ‘else if’, and is useful
to avoid excessive indentation.  An if … elif … elif … sequence is a substitute for the switch or case statements found in other languages.

If you’re comparing the same value to several constants, or checking for specific types or
attributes, you may also find the match statement useful. For more
details see match Statements .

4.2. for Statements</pre>

</details>

<details>
<summary>s04 — C — controlflow-007 — 1/2</summary>

[Trang nguồn](https://docs.python.org/3.13/tutorial/controlflow.html); vị trí ký tự 0–670 trong đơn vị.

<pre>&gt;&gt;&gt; fib
&lt;function fib at 10042ed0&gt;
&gt;&gt;&gt; f = fib
&gt;&gt;&gt; f(100)
0 1 1 2 3 5 8 13 21 34 55 89

Coming from other languages, you might object that fib is not a function but
a procedure since it doesn’t return a value.  In fact, even functions without a return statement do return a value, albeit a rather boring one.  This
value is called None (it’s a built-in name).  Writing the value None is
normally suppressed by the interpreter if it would be the only value written.
You can see it if you really want to using print() :

&gt;&gt;&gt; fib(0)
&gt;&gt;&gt; print(fib(0))
None

It is simple to write a function that returns a list of the numbers of the
Fibonacci series, instead of printing it:</pre>

</details>

<details>
<summary>s05 — C — controlflow-014 — 2/2</summary>

[Trang nguồn](https://docs.python.org/3.13/tutorial/controlflow.html); vị trí ký tự 0–918 trong đơn vị.

<pre>For Python, PEP 8 has emerged as the style guide that most projects adhere to;
it promotes a very readable and eye-pleasing coding style.  Every Python
developer should read it at some point; here are the most important points
extracted for you:

Use 4-space indentation, and no tabs. 4 spaces are a good compromise between small indentation (allows greater
nesting depth) and large indentation (easier to read).  Tabs introduce
confusion, and are best left out.

Wrap lines so that they don’t exceed 79 characters. This helps users with small displays and makes it possible to have several
code files side-by-side on larger displays.

Use blank lines to separate functions and classes, and larger blocks of
code inside functions.

When possible, put comments on a line of their own.

Use docstrings.

Use spaces around operators and after commas, but not directly inside
bracketing constructs: a = f(1, 2) + g(3, 4) .</pre>

</details>

<details>
<summary>s06 — C — datastructures-006 — 1/2</summary>

[Trang nguồn](https://docs.python.org/3.13/tutorial/datastructures.html); vị trí ký tự 0–975 trong đơn vị.

<pre>Here is a brief demonstration:

&gt;&gt;&gt; basket = {&#x27;apple&#x27;, &#x27;orange&#x27;, &#x27;apple&#x27;, &#x27;pear&#x27;, &#x27;orange&#x27;, &#x27;banana&#x27;}
&gt;&gt;&gt; print(basket)                      # show that duplicates have been removed
{&#x27;orange&#x27;, &#x27;banana&#x27;, &#x27;pear&#x27;, &#x27;apple&#x27;}
&gt;&gt;&gt; &#x27;orange&#x27; in basket                 # fast membership testing
True
&gt;&gt;&gt; &#x27;crabgrass&#x27; in basket
False

&gt;&gt;&gt; # Demonstrate set operations on unique letters from two words
&gt;&gt;&gt;
&gt;&gt;&gt; a = set(&#x27;abracadabra&#x27;)
&gt;&gt;&gt; b = set(&#x27;alacazam&#x27;)
&gt;&gt;&gt; a                                  # unique letters in a
{&#x27;a&#x27;, &#x27;r&#x27;, &#x27;b&#x27;, &#x27;c&#x27;, &#x27;d&#x27;}
&gt;&gt;&gt; a - b                              # letters in a but not in b
{&#x27;r&#x27;, &#x27;d&#x27;, &#x27;b&#x27;}
&gt;&gt;&gt; a | b                              # letters in a or b or both
{&#x27;a&#x27;, &#x27;c&#x27;, &#x27;r&#x27;, &#x27;d&#x27;, &#x27;b&#x27;, &#x27;m&#x27;, &#x27;z&#x27;, &#x27;l&#x27;}
&gt;&gt;&gt; a &amp; b                              # letters in both a and b
{&#x27;a&#x27;, &#x27;c&#x27;}
&gt;&gt;&gt; a ^ b                              # letters in a or b but not both
{&#x27;r&#x27;, &#x27;d&#x27;, &#x27;b&#x27;, &#x27;m&#x27;, &#x27;z&#x27;, &#x27;l&#x27;}

Similarly to list comprehensions , set comprehensions
are also supported:</pre>

</details>

<details>
<summary>s07 — C — errors-004 — 2/2</summary>

[Trang nguồn](https://docs.python.org/3.13/tutorial/errors.html); vị trí ký tự 0–681 trong đơn vị.

<pre>Exception handlers do not handle only exceptions that occur immediately in the try clause , but also those that occur inside functions that are called (even
indirectly) in the try clause . For example:

&gt;&gt;&gt; def this_fails():
...     x = 1/0
...
&gt;&gt;&gt; try:
...     this_fails()
... except ZeroDivisionError as err:
...     print(&#x27;Handling run-time error:&#x27;, err)
...
Handling run-time error: division by zero

8.4. Raising Exceptions

The raise statement allows the programmer to force a specified
exception to occur. For example:

&gt;&gt;&gt; raise NameError(&#x27;HiThere&#x27;)
Traceback (most recent call last):
  File &quot;&lt;stdin&gt;&quot;, line 1, in &lt;module&gt;
    raise NameError(&#x27;HiThere&#x27;)
NameError: HiThere</pre>

</details>

<details>
<summary>s08 — C — inputoutput-002 — 2/2</summary>

[Trang nguồn](https://docs.python.org/3.13/tutorial/inputoutput.html); vị trí ký tự 0–840 trong đơn vị.

<pre>Some examples:

&gt;&gt;&gt; s = &#x27;Hello, world.&#x27;
&gt;&gt;&gt; str(s)
&#x27;Hello, world.&#x27;
&gt;&gt;&gt; repr(s)
&quot;&#x27;Hello, world.&#x27;&quot;
&gt;&gt;&gt; str(1/7)
&#x27;0.14285714285714285&#x27;
&gt;&gt;&gt; x = 10 * 3.25
&gt;&gt;&gt; y = 200 * 200
&gt;&gt;&gt; s = &#x27;The value of x is &#x27; + repr(x) + &#x27;, and y is &#x27; + repr(y) + &#x27;...&#x27;
&gt;&gt;&gt; print(s)
The value of x is 32.5, and y is 40000...
&gt;&gt;&gt; # The repr() of a string adds string quotes and backslashes:
&gt;&gt;&gt; hello = &#x27;hello, world\n&#x27;
&gt;&gt;&gt; hellos = repr(hello)
&gt;&gt;&gt; print(hellos)
&#x27;hello, world\n&#x27;
&gt;&gt;&gt; # The argument to repr() may be any Python object:
&gt;&gt;&gt; repr((x, y, (&#x27;spam&#x27;, &#x27;eggs&#x27;)))
&quot;(32.5, 40000, (&#x27;spam&#x27;, &#x27;eggs&#x27;))&quot;

The string module contains a Template class that offers
yet another way to substitute values into strings, using placeholders like $x and replacing them with values from a dictionary, but offers much less
control of the formatting.

7.1.1. Formatted String Literals</pre>

</details>

<details>
<summary>s09 — C — modules-002 — 2/2</summary>

[Trang nguồn](https://docs.python.org/3.13/tutorial/modules.html); vị trí ký tự 0–959 trong đơn vị.

<pre>Each module has its own private namespace, which is used as the global namespace
by all functions defined in the module. Thus, the author of a module can
use global variables in the module without worrying about accidental clashes
with a user’s global variables. On the other hand, if you know what you are
doing you can touch a module’s global variables with the same notation used to
refer to its functions, modname.itemname .

Modules can import other modules.  It is customary but not required to place all import statements at the beginning of a module (or script, for that
matter).  The imported module names, if placed at the top level of a module
(outside any functions or classes), are added to the module’s global namespace.

There is a variant of the import statement that imports names from a
module directly into the importing module’s namespace.  For example:

&gt;&gt;&gt; from fibo import fib, fib2
&gt;&gt;&gt; fib(500)
0 1 1 2 3 5 8 13 21 34 55 89 144 233 377</pre>

</details>

<details>
<summary>s10 — C — modules-008 — 2/2</summary>

[Trang nguồn](https://docs.python.org/3.13/tutorial/modules.html); vị trí ký tự 0–672 trong đơn vị.

<pre>Be aware that submodules might become shadowed by locally defined names. For
example, if you added a reverse function to the sound/effects/__init__.py file, the from sound.effects import * would only import the two submodules echo and surround , but not the reverse submodule, because it is shadowed by the locally defined reverse function:

__all__ = [
    &quot;echo&quot;,      # refers to the &#x27;echo.py&#x27; file
    &quot;surround&quot;,  # refers to the &#x27;surround.py&#x27; file
    &quot;reverse&quot;,   # !!! refers to the &#x27;reverse&#x27; function now !!!
]

def reverse(msg: str):  # &lt;-- this name shadows the &#x27;reverse.py&#x27; submodule
    return msg[::-1]    #     in the case of a &#x27;from sound.effects import *&#x27;</pre>

</details>

## Grounding — 15 trường hợp

0: không có bằng chứng; 1: có bằng chứng nhưng thiếu điều kiện hoặc ngữ cảnh; 2: đủ để trả lời và truy nguồn. Chấm độ đủ của top-3, tách với metric so khớp gold tự động.

| Câu | Cấu hình | Điểm /2 | Hạng có bằng chứng | Đơn vị nguồn | Trích dẫn hỗ trợ | Lý do |
|---|---|---:|---:|---|---|---|
| q16 | A | 2 | 1 | classes-006 | Generally speaking, instance variables are for data unique to each instance<br>and class variables are for attributes and methods shared by all instances<br>of the class: | Top-3 có đoạn phân biệt dữ liệu riêng từng instance và thuộc tính/phương thức dùng chung của class. |
| q16 | B | 2 | 1 | classes-006 | Generally speaking, instance variables are for data unique to each instance<br>and class variables are for attributes and methods shared by all instances<br>of the class: | Top-3 có đoạn phân biệt dữ liệu riêng từng instance và thuộc tính/phương thức dùng chung của class. |
| q16 | C | 2 | 1 | classes-006 | Generally speaking, instance variables are for data unique to each instance<br>and class variables are for attributes and methods shared by all instances<br>of the class: | Top-3 có đoạn phân biệt dữ liệu riêng từng instance và thuộc tính/phương thức dùng chung của class. |
| q17 | A | 2 | 1 | classes-009 | Method references<br>are resolved as follows: the corresponding class attribute is searched,<br>descending down the chain of base classes if necessary, and the method reference<br>is valid if this yields a function object. | Hạng 1 có câu tìm thuộc tính tương ứng rồi đi theo chuỗi base class nếu cần; câu này đủ hỗ trợ đáp án. Riêng A bị trượt exact quote vì thiếu câu mở đầu về khởi tạo. |
| q17 | B | 2 | 1 | classes-009 | Method references<br>are resolved as follows: the corresponding class attribute is searched,<br>descending down the chain of base classes if necessary, and the method reference<br>is valid if this yields a function object. | Hạng 1 có câu tìm thuộc tính tương ứng rồi đi theo chuỗi base class nếu cần; câu này đủ hỗ trợ đáp án. Riêng A bị trượt exact quote vì thiếu câu mở đầu về khởi tạo. |
| q17 | C | 2 | 1 | classes-009 | Method references<br>are resolved as follows: the corresponding class attribute is searched,<br>descending down the chain of base classes if necessary, and the method reference<br>is valid if this yields a function object. | Hạng 1 có câu tìm thuộc tính tương ứng rồi đi theo chuỗi base class nếu cần; câu này đủ hỗ trợ đáp án. Riêng A bị trượt exact quote vì thiếu câu mở đầu về khởi tạo. |
| q18 | A | 2 | 2 | classes-010 | Any identifier of the form __spam (at least two leading underscores, at most one trailing underscore)<br>is textually replaced with _classname__spam , where classname is the<br>current class name with leading underscore(s) stripped. | Hạng 2 giữ đủ quy tắc __spam thành _classname__spam và cách bỏ gạch dưới đầu tên class. |
| q18 | B | 2 | 1 | classes-010 | Any identifier of the form __spam (at least two leading underscores, at most one trailing underscore)<br>is textually replaced with _classname__spam , where classname is the<br>current class name with leading underscore(s) stripped. | Hạng 1 giữ đủ quy tắc __spam thành _classname__spam và cách bỏ gạch dưới đầu tên class. |
| q18 | C | 2 | 1 | classes-010 | Any identifier of the form __spam (at least two leading underscores, at most one trailing underscore)<br>is textually replaced with _classname__spam , where classname is the<br>current class name with leading underscore(s) stripped. | Hạng 1 giữ đủ quy tắc __spam thành _classname__spam và cách bỏ gạch dưới đầu tên class. |
| q19 | A | 2 | 1 | classes-012 | When there are no more elements, __next__() raises a StopIteration exception which tells the for loop to terminate. | Có __next__, StopIteration và điều kiện hết phần tử, đủ trả lời và truy nguồn. |
| q19 | B | 2 | 1 | classes-012 | When there are no more elements, __next__() raises a StopIteration exception which tells the for loop to terminate. | Có __next__, StopIteration và điều kiện hết phần tử, đủ trả lời và truy nguồn. |
| q19 | C | 2 | 1 | classes-012 | When there are no more elements, __next__() raises a StopIteration exception which tells the for loop to terminate. | Có __next__, StopIteration và điều kiện hết phần tử, đủ trả lời và truy nguồn. |
| q20 | A | 2 | 1 | classes-012 | Generators are a simple and powerful tool for creating iterators.  They<br>are written like regular functions but use the yield statement<br>whenever they want to return data.  Each time next() is called on it, the<br>generator resumes where it left off (it remembers all the data values and which<br>statement was last executed).  An example shows that generators can be trivially<br>easy to create: | Có yield, next và việc tiếp tục tại trạng thái trước, đủ trả lời và truy nguồn. |
| q20 | B | 2 | 1 | classes-012 | Generators are a simple and powerful tool for creating iterators.  They<br>are written like regular functions but use the yield statement<br>whenever they want to return data.  Each time next() is called on it, the<br>generator resumes where it left off (it remembers all the data values and which<br>statement was last executed).  An example shows that generators can be trivially<br>easy to create: | Có yield, next và việc tiếp tục tại trạng thái trước, đủ trả lời và truy nguồn. |
| q20 | C | 2 | 1 | classes-012 | Generators are a simple and powerful tool for creating iterators.  They<br>are written like regular functions but use the yield statement<br>whenever they want to return data.  Each time next() is called on it, the<br>generator resumes where it left off (it remembers all the data values and which<br>statement was last executed).  An example shows that generators can be trivially<br>easy to create: | Có yield, next và việc tiếp tục tại trạng thái trước, đủ trả lời và truy nguồn. |

## Metadata — 45 bản ghi

Mỗi bản ghi được đối chiếu URL nguồn, page/unit, chapter, version, language và đoạn ký tự của chunk với snapshot. Kết quả kiểm bằng script đã được Trần Văn Quang đọc lại và xác nhận thủ công. Metadata đúng không đồng nghĩa thứ hạng truy xuất đúng hoặc tuân thủ phạm vi khi cấu hình không bật filter.

| Câu | Cấu hình | Hạng | Trang nguồn | Page | Chapter | Kết quả |
|---|---|---:|---|---:|---|---|
| q16 | A | 1 | [Nguồn](https://docs.python.org/3.13/tutorial/classes.html) | 6 | classes | Đủ và đúng |
| q16 | A | 2 | [Nguồn](https://docs.python.org/3.13/tutorial/controlflow.html) | 4 | controlflow | Đủ và đúng |
| q16 | A | 3 | [Nguồn](https://docs.python.org/3.13/tutorial/classes.html) | 5 | classes | Đủ và đúng |
| q16 | B | 1 | [Nguồn](https://docs.python.org/3.13/tutorial/classes.html) | 6 | classes | Đủ và đúng |
| q16 | B | 2 | [Nguồn](https://docs.python.org/3.13/tutorial/classes.html) | 7 | classes | Đủ và đúng |
| q16 | B | 3 | [Nguồn](https://docs.python.org/3.13/tutorial/classes.html) | 8 | classes | Đủ và đúng |
| q16 | C | 1 | [Nguồn](https://docs.python.org/3.13/tutorial/classes.html) | 6 | classes | Đủ và đúng |
| q16 | C | 2 | [Nguồn](https://docs.python.org/3.13/tutorial/classes.html) | 7 | classes | Đủ và đúng |
| q16 | C | 3 | [Nguồn](https://docs.python.org/3.13/tutorial/classes.html) | 8 | classes | Đủ và đúng |
| q17 | A | 1 | [Nguồn](https://docs.python.org/3.13/tutorial/classes.html) | 9 | classes | Đủ và đúng |
| q17 | A | 2 | [Nguồn](https://docs.python.org/3.13/tutorial/classes.html) | 8 | classes | Đủ và đúng |
| q17 | A | 3 | [Nguồn](https://docs.python.org/3.13/tutorial/classes.html) | 9 | classes | Đủ và đúng |
| q17 | B | 1 | [Nguồn](https://docs.python.org/3.13/tutorial/classes.html) | 9 | classes | Đủ và đúng |
| q17 | B | 2 | [Nguồn](https://docs.python.org/3.13/tutorial/classes.html) | 9 | classes | Đủ và đúng |
| q17 | B | 3 | [Nguồn](https://docs.python.org/3.13/tutorial/classes.html) | 9 | classes | Đủ và đúng |
| q17 | C | 1 | [Nguồn](https://docs.python.org/3.13/tutorial/classes.html) | 9 | classes | Đủ và đúng |
| q17 | C | 2 | [Nguồn](https://docs.python.org/3.13/tutorial/classes.html) | 9 | classes | Đủ và đúng |
| q17 | C | 3 | [Nguồn](https://docs.python.org/3.13/tutorial/classes.html) | 9 | classes | Đủ và đúng |
| q18 | A | 1 | [Nguồn](https://docs.python.org/3.13/tutorial/classes.html) | 10 | classes | Đủ và đúng |
| q18 | A | 2 | [Nguồn](https://docs.python.org/3.13/tutorial/classes.html) | 10 | classes | Đủ và đúng |
| q18 | A | 3 | [Nguồn](https://docs.python.org/3.13/tutorial/modules.html) | 5 | modules | Đủ và đúng |
| q18 | B | 1 | [Nguồn](https://docs.python.org/3.13/tutorial/classes.html) | 10 | classes | Đủ và đúng |
| q18 | B | 2 | [Nguồn](https://docs.python.org/3.13/tutorial/classes.html) | 9 | classes | Đủ và đúng |
| q18 | B | 3 | [Nguồn](https://docs.python.org/3.13/tutorial/classes.html) | 11 | classes | Đủ và đúng |
| q18 | C | 1 | [Nguồn](https://docs.python.org/3.13/tutorial/classes.html) | 10 | classes | Đủ và đúng |
| q18 | C | 2 | [Nguồn](https://docs.python.org/3.13/tutorial/classes.html) | 9 | classes | Đủ và đúng |
| q18 | C | 3 | [Nguồn](https://docs.python.org/3.13/tutorial/classes.html) | 11 | classes | Đủ và đúng |
| q19 | A | 1 | [Nguồn](https://docs.python.org/3.13/tutorial/classes.html) | 12 | classes | Đủ và đúng |
| q19 | A | 2 | [Nguồn](https://docs.python.org/3.13/tutorial/classes.html) | 12 | classes | Đủ và đúng |
| q19 | A | 3 | [Nguồn](https://docs.python.org/3.13/tutorial/controlflow.html) | 2 | controlflow | Đủ và đúng |
| q19 | B | 1 | [Nguồn](https://docs.python.org/3.13/tutorial/classes.html) | 12 | classes | Đủ và đúng |
| q19 | B | 2 | [Nguồn](https://docs.python.org/3.13/tutorial/classes.html) | 12 | classes | Đủ và đúng |
| q19 | B | 3 | [Nguồn](https://docs.python.org/3.13/tutorial/controlflow.html) | 2 | controlflow | Đủ và đúng |
| q19 | C | 1 | [Nguồn](https://docs.python.org/3.13/tutorial/classes.html) | 12 | classes | Đủ và đúng |
| q19 | C | 2 | [Nguồn](https://docs.python.org/3.13/tutorial/classes.html) | 12 | classes | Đủ và đúng |
| q19 | C | 3 | [Nguồn](https://docs.python.org/3.13/tutorial/controlflow.html) | 2 | controlflow | Đủ và đúng |
| q20 | A | 1 | [Nguồn](https://docs.python.org/3.13/tutorial/classes.html) | 12 | classes | Đủ và đúng |
| q20 | A | 2 | [Nguồn](https://docs.python.org/3.13/tutorial/classes.html) | 12 | classes | Đủ và đúng |
| q20 | A | 3 | [Nguồn](https://docs.python.org/3.13/tutorial/classes.html) | 13 | classes | Đủ và đúng |
| q20 | B | 1 | [Nguồn](https://docs.python.org/3.13/tutorial/classes.html) | 12 | classes | Đủ và đúng |
| q20 | B | 2 | [Nguồn](https://docs.python.org/3.13/tutorial/classes.html) | 13 | classes | Đủ và đúng |
| q20 | B | 3 | [Nguồn](https://docs.python.org/3.13/tutorial/classes.html) | 12 | classes | Đủ và đúng |
| q20 | C | 1 | [Nguồn](https://docs.python.org/3.13/tutorial/classes.html) | 12 | classes | Đủ và đúng |
| q20 | C | 2 | [Nguồn](https://docs.python.org/3.13/tutorial/classes.html) | 13 | classes | Đủ và đúng |
| q20 | C | 3 | [Nguồn](https://docs.python.org/3.13/tutorial/classes.html) | 12 | classes | Đủ và đúng |

## Hồ sơ gốc

- [Nhãn coherence và chunk đầy đủ](coherence_audit.jsonl)
- [Nhãn grounding và bằng chứng](grounding_audit.jsonl)
- [Đối chiếu metadata](metadata_audit.jsonl)
- [Kết quả tổng hợp](quality_summary.json)
- [Trace test](traces_test.jsonl)
- [Báo cáo và phân tích năm khía cạnh](../report/individual/2A202604032_TranVanQuang.md)
