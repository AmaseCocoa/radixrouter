/*
* Test for C++ RadixTree performance.
* `get` run 10000000 times, about 70 seconds
*/

#include <iostream>
#include <time.h>
#include <memory>

#include "tree.h"

using std::cout;
using std::endl;
using std::shared_ptr;
using std::make_shared;

using radixtree::RadixTree;
using radixtree::Request;
using radixtree::HandleFunc;

auto handle = [](shared_ptr<Request> req) {
  cout << "Handled! The params are:" << endl;
  for (auto &param : req->params)
    cout << param.first << ": " << param.second << endl;
};

RadixTree tree;
auto req = make_shared<Request>("/user/Lime/male/25", "GET");

void testWork() {
  bool pathExisted;
  HandleFunc handler;

  cout << tree.insert("/user", handle, {"GET"}) << endl;
  cout << tree.insert("/user/:name", handle, {"GET"}) << endl;
  cout << tree.insert("/user/:name", handle, {"POST"}) << endl;
  cout << tree.insert("/user/:name/:sex/:age", handle, {"GET"}) << endl;
  cout << tree.insert("/user/lime", handle, {"GET"}) << endl;
  cout << tree.insert("/src/*filename", handle, {"GET"}) << endl;
  cout << tree.insert("/src/image.png", handle, {"GET"}) << endl << endl;

  tie(pathExisted, handler, req->params) = tree.get(req->path, req->method);

  cout << pathExisted << endl;
  if (handler)
    handler(req);
}

void testPerformance() {
  auto start = clock();
  for (auto i = 0; i < 10000000; i++)
    tree.get(req->path, req->method);

  cout << "Total cost " << (clock() - start) * 1.0 / CLOCKS_PER_SEC
       << "seconds" << endl;
}

int main() {
  testWork();
  testPerformance();
}
