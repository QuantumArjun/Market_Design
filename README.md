# Market_Design

Coding up some of the algorithms from Stanford's CS 136

## Gale Shapley

Input the preferences of the two sides under `preferences.json`

Here is the format for the preferences: 
```
{
    "left": {
        "1": {
            "ranking": "1, 2, 3"
        },
        "2": {
            "ranking": "1, 2, 3"
        },
        "3": {
            "ranking": "1, 2, 3"
        }
    },
  
    "right": {
        "1": {
            "ranking": "1, 2, 3"
          },
        "2": {
            "ranking": "1, 2, 3"
        },
        "3": {
            "ranking": "1, 2, 3"
        }
  }
}
```

To run Deferred Acceptance (also known as Gale-Shapley), run the following command to run the left proposing DA algorithm:
'python main.py --algorithm DA --proposing left'
  
