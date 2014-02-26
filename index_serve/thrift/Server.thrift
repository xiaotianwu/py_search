namespace cpp index_serving
namespace py index_serving

enum IndexServingStatus {
  OFFLINE = 1,
  PREPARE = 2,
  ONLINE = 3,
  ERROR = 4
}

struct IndexServingProperty {
  1: string name, // unique server name
  2: IndexServingStatus status,
  3: optional i32 row,
  4: optional i32 col,
  5: optional i32 payload
}

service IndexServing {

   IndexServingProperty ping(),

   // return match doc ids
   list<i32> search(1:list<i32> termIds),

   // test method, passing string list cost too much
   list<i32> search_terms(1:list<string> terms)
}
