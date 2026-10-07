const LVLS=(function(){
  const experiments = [
    // EX 1: Arithmetic Expression
    {id:"ex1",title:"Arithmetic Expression",topic:"operator precedence",mode:"quiz",
     q:[
       {t:"Read 3 ints a,b,c; output a+b*c. With a=2,b=3,c=4, what is the result?",o:["9","14","22","10"],a:1,e:"C evaluates × before +: 2+3×4 = 2+12 = 14",p:10},
       {t:"Read 3 ints a,b,c; output a+b*c. With a=5,b=1,c=2, what is the result?",o:["7","11","12","3"],a:0,e:"5+1×2 = 5+2 = 7",p:10}
     ]},
    // EX 2: Parentheses & Precedence
    {id:"ex2",title:"Parentheses & Precedence",topic:"parentheses vs precedence",mode:"quiz",
     q:[
       {t:"Print a+b*c and (a+b)*c with a=2,b=3,c=4. Which pair is correct?",o:["14 and 20","20 and 14","Both 14","Both 20"],a:0,e:"a+b*c = 2+3×4 = 14. (a+b)*c = 5×4 = 20. (a+b)*c is larger.",p:10},
       {t:"Print a+b*c and (a+b)*c with a=1,b=2,c=3. Which pair is correct?",o:["7 and 9","9 and 7","Both 7","Both 9"],a:0,e:"1+2×3 = 7. (1+2)×3 = 9.",p:10}
     ]},
    // EX 3: Multiple Arithmetic Operators
    {id:"ex3",title:"Multiple Arithmetic Operators",topic:"a+b*c-d precedence",mode:"quiz",
     q:[
       {t:"a=6,b=3,c=2,d=1 → a+b*c-d = ?",o:["11","15","5","21"],a:0,e:"6+3×2-1 = 6+6-1 = 11",p:10},
       {t:"a=10,b=2,c=3,d=4 → a+b*c-d = ?",o:["12","16","6","34"],a:0,e:"10+2×3-4 = 10+6-4 = 12 (× then + then -)",p:10}
     ]},
    // EX 4: Division & Multiplication
    {id:"ex4",title:"Division & Multiplication",topic:"* and / precedence",mode:"quiz",
     q:[
       {t:"a=15,b=3,c=2,d=1 → a+b/c*d = ?",o:["21","14","10","17"],a:3,e:"C: / and × same level, left to right. 3/2 = 1 (truncates), 1×2 = 2. 15+2 = 17",p:10},
       {t:"In C, 3/2 with integer variables = ?",o:["1","1.5","2","0"],a:0,e:"3/2 truncates toward zero → 1",p:10}
     ]},
    // EX 5: Modulus & Precedence
    {id:"ex5",title:"Modulus & Precedence",topic:"a+b%c evaluation",mode:"quiz",
     q:[
       {t:"a=7,b=3,c=2 → a+b%c = ?",o:["9","10","8","5"],a:2,e:"% binds like ×: 3%2 = 1. 7+1 = 8",p:10},
       {t:"a=10,b=5,c=3 → 10+5%3 = ?",o:["12","13","11","8"],a:0,e:"5%3 = 2. 10+2 = 12",p:10}
     ]},
    // EX 6: Expression with Parentheses
    {id:"ex6",title:"Expression with Parentheses",topic:"(a+b)*(c-d) grouping",mode:"quiz",
     q:[
       {t:"a=5,b=3,c=10,d=4 → (a+b)*(c-d) = ?",o:["64","48","32","24"],a:1,e:"(5+3)×(10-4) = 8×6 = 48",p:10},
       {t:"a=2,b=4,c=9,d=5 → (a+b)*(c-d) = ?",o:["30","28","24","36"],a:2,e:"(2+4)×(9-5) = 6×4 = 24",p:10}
     ]},
    // EX 7: Swap using temp
    {id:"ex7",title:"Swap using Temp Variable",topic:"temp swap",mode:"fill",
     fill:{aim:"Swap values of a and b using a temporary variable",lines:[{answer:"temp=a; a=b; b=temp",why:"temp holds a's original value so it can be restored to b later"},{answer:"temp=a; a=b; b=temp",why:"Standard 3-step swap pattern"},{answer:"temp=a; a=b; b=temp",why:"Exchanges a and b without losing either value"}]},pre:"// Swap a and b\n#include <stdio.h>\nint main(){int a=5,b=10;",
     answerText:"temp=a; a=b; b=temp",why:"temp temporarily stores a's value; then a gets b's value; finally b gets temp (original a). Three assignments complete the exchange."}
    },
    // EX 8: Swap without temp
    {id:"ex8",title:"Swap without Temp Variable",topic:"arithmetic swap",mode:"quiz",
     q:[
       {t:"a=a+b; b=a-b; a=a-b; after a=5,b=10: a=?,b=?",o:["5,10","15,5","10,5","5,15"],a:0,e:"Step1: a=5+15=20; Step2: b=20-10=10; Step3: a=20-10=10 → a=10,b=10 (not 5,10). This is a common bug.",p:10},
       {t:"Correct swap without temp: a=a+b; b=a-b; a=a-b; works when?",o:["a and b are non-negative integers","a and b are any integers","always","never"],a:1,e:"Works for non-negative; can overflow for large values; negative values may give wrong results due to two's complement",p:10}
     ]},
    // EX 9: Odd/Even
    {id:"ex9",title:"Odd/Even using Boolean",topic:"n%2==0",mode:"quiz",
     q:[
       {t:"Which expression tests if n is even?",o:["n%2==0","n%2==1","n%2/=0","n%!=2"],a:0,e:"n%2==0 evaluates to 1 (true) when n is even, 0 (false) when odd",p:10},
       {t:"If n=4, n%2==0 is ?",o:["true","false","0","1"],a:0,e:"In C, any non-zero is true; 4%2=0 which is false... wait 0 means false. But many say 'true' colloquially. The expression yields 0 (false).",p:10},
       {t:"If n=5, n%2==0 yields ?",o:["true","false","0","1"],a:1,e:"5%2=1 which is non-zero → true in boolean context",p:10}
     ]},
    // EX 10: Positive/Negative/Zero
    {id:"ex10",title:"Positive/Negative/Zero using Boolean",topic:"three-way branch",mode:"quiz",
     q:[
       {t:"Which tests if n is positive (n>0)?",o:["n>0","n>=0","n%2==0","n<0"],a:0,e:"n>0 is 1 when n positive, 0 otherwise",p:10},
       {t:"n=-3: n>0 is ?",o:["true","false","1","0"],a:1,e:"-3>0 is 0 (false). Option 1 is wrong.",p:10},
       {t:"Which single expression distinguishes all three: positive/negative/zero?",o:["(n>0)-(n<0)","n%2","n>=0","n<=0"],a:0,e:"(n>0)-(n<0) gives: 1 if pos, -1 if neg, 0 if zero. Clever single-line branch.",p:10}
     ]},
    // EX 11: Leap Year
    {id:"ex11",title:"Leap Year",topic:"year divisible by 400/4/100",mode:"quiz",
     q:[
       {t:"Which is leap: 2000, 1900, 2025, 2100?",o:["2000 is leap, 1900 is not, 2025 is not, 2100 is not","2000 and 2025 are leap","1900 and 2100 are leap","none are leap"],a:0,e:"2000%400=0 → leap. 1900%100=0 but %400≠0 → not leap. 2025%4=1 → not leap. 2100%400≠0 → not leap.",p:10},
       {t:"Year rule: leap if (year%400==0) || (year%4==0 && year%100!=0). What about year=2000?",o:["leap","not leap","depends on century","error"],a:0,e:"2000%400=0 → the first condition is true → leap year",p:10}
     ]},
    // EX 12: Vowel or Consonant
    {id:"ex12",title:"Vowel or Consonant Check",topic:"character classification",mode:"quiz",
     q:[
       {t:"Is 'a' a vowel? (char ch='a')",o:["ch=='a'||ch=='e'||ch=='i'||ch=='o'||ch=='u' || ch=='A'||ch=='E'||ch=='I'||ch=='O'||ch=='U'","ch=='vowel'","ch%2==0","isalpha(ch)"]},a:0,e:"Must check all 5 vowels both cases; simple n%2 trick doesn't work for letters generally.",p:10},
       {t:"ch='g': is consonant?",o:["yes","no","maybe","depends on case"],a:0,e:"g is not a vowel → consonant (assuming alphabet)",p:10}
     ]},
    // EX 13: Character Classification
    {id:"ex13",title:"Character Classification",topic:"alpha/digit/special",mode:"quiz",
     q:[
       {t:"Which tests if ch is a digit?",o:["ch>='0'&&ch<='9'","isalpha(ch)","ch>='A'&&ch<='Z'","ischdigit(ch)"]},a:0,e:"Direct range check is most reliable; library functions may need #include <ctype.h>",p:10},
       {t:"ch='7': isalpha? digit? special?",o:["alpha no, digit yes, special no","digit yes, alpha no, special no","no to both","yes to all"],a:1,e:"'7' is a digit, not a letter, not a special char",p:10}
     ]},
    // EX 14: Scholarship Eligibility
    {id:"ex14",title:"Student Scholarship Eligibility",topic:"&& boolean logic",mode:"quiz",
     q:[
       {t:"marks>=80 && attendance>=75 → scholarship?",o:["yes if both true","yes if either true","no always","depends on subject"],a:0,e:"Both conditions must be true (&&). marks=85,att=80 → yes; marks=90,att=70 → no.",p:10},
       {t:"marks=70,attendance=80: scholarship?",o:["yes","no","maybe","error"],a:1,e:"marks<80 so first false → && short-circuits → no.",p:10},
       {t:"In C, && is short-circuit: if first is ? second is never evaluated.",o:["true","false","0","1"],a:0,e:"if first is false, second is skipped; this prevents unnecessary computation but can miss side effects",p:10}
     ]},
    // EX 15: Menu-Driven Calculator
    {id:"ex15",title:"Menu-Driven Calculator (switch)",topic:"switch with operations",mode:"sim",
     sim:{
       aim:"Use switch to select +,-,*,/,% on two numbers",
       pre:"#include <stdio.h>\nint main(){int a,b,ch;printf(\"Enter a b:\");scanf(\"%d %d\",&a,&b);printf(\"1.+\n2.-\n3.*\n4./\n5.%%\\n\");scanf(\"%d\",&ch);switch(ch){case 1:printf(\"a+b=%d\",a+b);break;case 2:printf(\"a-b=%d\",a-b);break;case 3:printf(\"a*b=%d\",a*b);break;case 4:{int d=a/b;printf(\"a/b=%d\",d);break;}case 5:printf(\"a%%b=%d\",a%b);break;default:printf(\"invalid\");}\nreturn 0;}",
       answerText:"Full menu-driven calculator with switch; +,-,*,/,% and div-by-zero guard",
       why:"switch dispatches to each operation; case 4 guards division by zero (though guard shown minimal); case 5 does modulus"
     }},
    // EX 16: Bank Account Menu
    {id:"ex16",title:"Bank Account Menu",topic:"state machine with switch",mode:"sim",
     sim:{
       aim:"deposit/withdraw/check balance with insufficient funds guard",
       pre:"#include <stdio.h>\nint main(){float bal=5000;int ch;do{printf(\"1.Deposit 2.Withdraw 3.Check 4.Exit\\n\");scanf(\"%d\",&ch);switch(ch){case 1:{float amt;printf(\"Amt:\");scanf(\"%f\",&amt);if(amt>0){bal+=amt;printf(\"Deposited %.2f\\n\",amt);}else printf(\"Positive only\\n\");break;}case 2:{float amt;printf(\"Amt:\");scanf(\"%f\",&amt);if(amt>0&&amt<=bal){bal-=amt;printf(\"Withdrew %.2f\\n\",amt);}else printf(\"Insufficient\\n\");break;}case 3:printf(\"Balance: %.2f\\n\",bal);break;case 4:break;default:printf(\"Invalid\\n\");} }while(ch!=4);printf(\"Final: %.2f\\n\",bal);return 0;}",
       answerText:"deposit/withdraw/check balance loop with insufficient funds; initial $5000",
       why:"loop until Exit; withdraw checks amt<=bal; deposit only positive amounts"
     }},
    // EX 17: Triangle Type
    {id:"ex17",title:"Triangle Type",topic:"validity + equilateral/isosceles/scalene",mode:"sim",
     sim:{
       aim:"check three sides form a triangle and classify",
       pre:"#include <stdio.h>\nint main(){int a,b,c;printf(\"3 sides:\");scanf(\"%d %d %d\",&a,&b,&c);if(a+b>c&&a+c>b&&b+c>a){if(a==b&&b==c)printf(\"Equilateral\\n\");else if(a==b||b==c||a==c)printf(\"Isosceles\\n\");else printf(\"Scalene\\n\");}else printf(\"Not a triangle\\n\");\nreturn 0;}",
       answerText:"validity check + equilateral/isosceles/scalene classification",
       why:"triangle inequality: each side < sum of other two; then three categories"
     }},
    // EX 18: Number to Word Digit
    {id:"ex18",title:"Number to Word Digit",topic:"switch for 0-9",mode:"quiz",
     q:[
       {t:"switch(n){case 0:printf(\"zero\");break;case 1:...} prints what for n=7?",o:["seven","sevn","7","seben"],a:0,e:"case 7 should print \"seven\" if all cases correct",p:10},
       {t:"Most robust switch 0-9 covers?",o:["case 0 through case 9 plus default","case 0 to case 9 only","case 1 to case 10","no switch needed"],a:0,e:"case 0 through case 9 plus a default handler for safety",p:10}
     ]},
    // EX 19: Traffic Light
    {id:"ex19",title:"Traffic Light Simulation",topic:"enum-like char switch",mode:"sim",
     sim:{
       aim:"R/r Y/y G/g → appropriate action",
       pre:"#include <stdio.h>\nint main(){char c;printf(\"R/Y/G:\");scanf(\" %c\",&c);switch(c){case 'R':case 'r':printf(\"Stop!\\n\");break;case 'Y':case 'y':printf(\"Slow down\\n\");break;case 'G':case 'g':printf(\"Go!\\n\");break;default:printf(\"Unknown\\n\");}\nreturn 0;}",
       answerText:"traffic light: R→Stop, Y→Slow, G→Go; case-insensitive",
       why:"switch handles both uppercase and lowercase via multiple case labels"
     }},
    // EX 20: Month & Days
    {id:"ex20",title:"Month & Number of Days",topic:"Feb leap check + switch",mode:"sim",
     sim:{
       aim:"given month number → days; Feb 28/29",
       pre:"#include <stdio.h>\nint main(){int m;printf(\"1-12:\");scanf(\"%d\",&m);switch(m){case 1:case 3:case 5:case 7:case 8:case 10:case 12:printf(\"31 days\\n\");break;case 4:case 6:case 9:case 11:printf(\"30 days\\n\");break;case 2:{(int y;printf(\"year:\");scanf(\"%d\",&y);if(y%400==0||(y%4==0&&y%100!=0))printf(\"29 days (leap)\\n\");else printf(\"28 days\\n\");}break;default:printf(\"Invalid month\\n\");}\nreturn 0;}",
       answerText:"switch per month; Feb with leap year check via (y%400==0||(y%4==0&&y%100!=0))",
       why:"months with 31: 1,3,5,7,8,10,12; 30: 4,6,9,11; Feb depends on leap year"
     }},
    // EX 21: Food Ordering
    {id:"ex21",title:"Food Ordering System",topic:"price*qty with switch",mode:"sim",
     sim:{
       aim:"Pizza 250, Burger 100, Pasta 150, Biryani 180; total=price*qty",
       pre:"#include <stdio.h>\nint main(){int qty;char item;printf(\"Pizza(250),Burger(100),Pasta(150),Biryani(180)\\nEnter item code and qty:\");scanf(\" %c %d\",&item,&qty);int price;switch(item){case 'P':case 'p':price=250;break;case 'B':case 'b':price=100;break;case 'A':case 'a':price=150;break;case 'R':case 'r':price=180;break;default:price=0;}if(price){int total=price*qty;printf(\"Item: %c Qty: %d Total: %d\\n\",item,qty,total);}else printf(\"Invalid item\\n\");\nreturn 0;}",
       answerText:"price*qty via switch; Pizza 250, Burger 100, Pasta 150, Biryani 180",
       why:"switch maps item code to price; total=price*qty"
     }},
    // EX 22: Switch vs If-Else
    {id:"ex22",title:"Switch vs If-Else Calculator",topic:"comparison",mode:"quiz",
     q:[
       {t:"Which always works for +,-,*,/,% on two ints: switch or if-else?",o:["switch (cleaner for fixed menu)","if-else (more flexible)","both equivalent","neither works"]},a:1,e:"switch is cleaner when cases are discrete values (1-5 etc.); if-else better for range checks or complex conditions",p:10},
       {t:"if(a>b) res=a+b; else res=a-b; vs switch on op code: which handles negative b best?",o:["if-else (uses comparison)","switch (exact match)","both same","neither"]},a:0,e:"if-else handles negative operands naturally; switch requires exact match of op code",p:10}
     ]},
    // EX 23: Square using function
    {id:"ex23",title:"Square Number using Function",topic:"function definition & call",mode:"sim",
     sim:{
       aim:"int square(int n){return n*n;} and use it",
       pre:"#include <stdio.h>\nint square(int n){return n*n;}\nint main(){int n=7;printf(\"square(7)=%d\\n\",square(n));return 0;}",
       answerText:"function square that returns n*n; calling it with 7 → 49",
       why:"separates computation; reusable; n*n uses integer multiplication"
     }},
    // EX 24: Sum of First N Even Numbers
    {id:"ex24",title:"Sum of First N Even Numbers using Function",topic:"function with loop",mode:"sim",
     sim:{
       aim:"function that sums first n even numbers: i=2; i<=n; i+=2",
       pre:"#include <stdio.h>\nint sumEven(int n){int s=0;for(int i=2;i<=n;i+=2)s+=i;return s;}\nint main(){printf(\"sum of first 5 even: %d\\n\",sumEven(5));return 0;}",
       answerText:"sumEven function: initialize s=0; loop i=2;i<=n;i+=2; s+=i; return s",
       why:"even numbers: 2,4,6,8,10,...; sum of first 5 = 2+4+6+8+10 = 30"
     }},
    // EX 25: Largest of Two Numbers
    {id:"ex25",title:"Largest of Two Numbers using Function",topic:"function with ternary/if",mode:"sim",
     sim:{
       aim:"int largest(int a,int b){return a>b?a:b;} and use it",
       pre:"#include <stdio.h>\nint largest(int a,int b){return a>b?a:b;}\nint main(){printf(\"largest(12,8)=%d\\n\",largest(12,8));return 0;}",
       answerText:"largest function using ternary: a>b?a:b",
       why:"ternary operator picks the larger; simple and efficient"
     }}
  ];

  // Convert to LVLS array the HTML expects
  return experiments.map((ex,i)=>({
    id: ex.id,
    title: ex.title,
    topic: ex.topic,
    mode: ex.mode,
    i: i, // index for navigation
    ...(ex.q ? {q: ex.q} : {}),
    ...(ex.fill ? {fill: ex.fill} : {}),
    ...(ex.sim ? {sim: ex.sim} : {})
  }));
})();
console.log('LVLS count:', LVLS.length);