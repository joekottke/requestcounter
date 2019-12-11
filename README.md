# requestcounter
A simple web application that counts requests in an accumulator.  Used for teaching counters -> rates

## Build and Run
The easiest way to build and run this simple app is to use Docker. From within your checkout of the repo:

```sh
docker build -t requestcounter .
```

And to run it:

```sh
docker run -it -p 5555:5555 requestcounter
```

