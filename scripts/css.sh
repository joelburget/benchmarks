#!/bin/bash
# Run from root of project
# $ ./scripts.css.sh
cd assets/css
scp *.css benchmarkweb@syrus.cse.ohio-state.edu:/home/benchmarkweb/benchmarks/assets/css/
cd -
