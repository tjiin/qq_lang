## QQLang (because _tears_)
A simple personal project creating a programming language in python. The gaol was to to explore language theory, parsing and syntax

### So...What is it good for?
"Absolutely nothing!"
In all seriousness, it's only useful as a toy/educational example. It's fun trying to define your own syntax constructs.

### I estimate it's about 100-200 times slower than C...

That said, I learned a ton about the process of writing a programming language and indeed to purse the idea further, perhaps with a more efficient base language.

### Syntax Examples

```
// factorial defined as an implicit conditional expression (note the lack of a return statement)

factorial(x) => {
    x ? x*factorial(x-1) : 1;
}
factorial(10);

// Or how about factorial as a switch statement?

factorial(x) => {
    switch (x) {
        case 0:
            return 1;
        default:
            return x*factorial(x-1);
    }
}
factorial(10);

// And just for the fun (and horror) of it, I added goto statements..
// Here's factorial written with goto

f(x) => {
    let p = x;
    @dec: x = x-1;
    p = p*x;
    if x != 1 { goto @dec; }
    return p;
}
f(10);
```
