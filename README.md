## QQLang (because _tears_)
A personal project writing my own programming language in Python. The main motivation was just wanting to know more about how programming languages work and how they are created.

### "So...What is it good for?"
"Absolutely nothing!" haha

It's only useful as a toy or learning example. I've had some great fun coming up with different syntax and grammar ideas and spent a lot of time looking different languages for things I thought were interesting or novel.
There's a pretty heavy javascript influence, most notably the ES6 arrow notation.
The language is still **very** barebones. There are no strings, lists, objects or datatypes other than numbers and booleans.

### I estimate it's about 100-200 times slower than C...
That said, I learned a ton in the process and had a lot of fun. 


### Misc Features
* optional static typing: let, const, int, float, bool
* first-class functions
* switch statements
* ternary operator
* "spacehsip" operator
* self-calling functions
* goto! :D

### Some Syntax Examples


```javascript

// Passing a function as an argument
f(g,x) => { return g(x) } 
g(y) => y*-10; 
f(g,2);         // -20


// Returning a function
f() => { g(x) => x*-3; return(g); } 
let h = f(); 
h(2);           // -6

// Definining a function with closures
f(x) => g(y) => x + y; 
let h = f(2); 
h(10);          // 12

// Assigning to a function definition
let f = g(x) => x*2; 
f(-1);         // -2

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
// So here's factorial written with goto.
f(x) => {
    let p = x;
    @dec: x = x-1;
    p = p*x;
    if x != 1 { goto @dec; }
    return p;
}
f(10);
```
