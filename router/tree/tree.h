/*
* Radix Tree in C++
*/

#ifndef TREE_H
#define TREE_H

#include <string>
#include <vector>
#include <unordered_map>
#include <tuple>
#include <memory>

namespace radixtree {

using std::string;
using std::vector;
using std::unordered_map;
using std::tuple;
using std::shared_ptr;
using std::make_shared;

struct Request {
  string path;
  string method;
  unordered_map<string, string> params;

  Request(string path, string method);
};

typedef void (*HandleFunc)(shared_ptr<Request>);
typedef tuple<bool, HandleFunc, unordered_map<string, string>> ParseResult;

const char ASTERISK = '*';
const char COLON = ':';
const char SLASH = '/';

struct RadixTreeNode {
  string path;
  unordered_map<string, HandleFunc> methods;
  unordered_map<char, shared_ptr<RadixTreeNode>> children;

  RadixTreeNode() = default;
  RadixTreeNode(string path);
  int addMethods(const vector<string> &methods, HandleFunc handler);
};

class RadixTree {
public:
  RadixTree();
  int insert(const string &key, HandleFunc handler,
             const vector<string> &methods);
  ParseResult get(const string &key, const string &method);
private:
  shared_ptr<RadixTreeNode> root;
  inline int getpos(int i, int n) {
    return (((i) + 1) % (n + 1) + n) % (n + 1);
  };
};

}  // namespace radixtreee

#endif
