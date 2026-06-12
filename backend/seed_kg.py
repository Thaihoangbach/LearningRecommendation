from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()
driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"),
    auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
)

def seed():
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")  # xóa data cũ

        # --- Domains ---
        session.run("CREATE (:Domain {id:'cs', name:'Computer Science'})")
        session.run("CREATE (:Domain {id:'health', name:'Digital Health'})")

        # --- Courses ---
        courses = [
            {"id":"python_basics",    "title":"Python for Beginners",        "difficulty":"beginner",     "hours":20, "domain":"cs",     "desc":"Nền tảng lập trình Python",            "outcomes":"Viết script, xử lý file, dùng thư viện cơ bản"},
            {"id":"data_analysis",    "title":"Data Analysis with Python",   "difficulty":"intermediate", "hours":30, "domain":"cs",     "desc":"Phân tích dữ liệu với Pandas/NumPy",   "outcomes":"Làm sạch, phân tích, trực quan hóa dữ liệu"},
            {"id":"data_viz",         "title":"Data Visualization",          "difficulty":"intermediate", "hours":25, "domain":"cs",     "desc":"Biểu đồ và dashboard chuyên nghiệp",   "outcomes":"Thiết kế dashboard, kể chuyện bằng dữ liệu"},
            {"id":"machine_learning", "title":"Machine Learning Basics",     "difficulty":"advanced",     "hours":40, "domain":"cs",     "desc":"Thuật toán ML cơ bản",                 "outcomes":"Xây dựng và đánh giá mô hình ML"},
            {"id":"db_management",    "title":"Database Management",         "difficulty":"intermediate", "hours":28, "domain":"cs",     "desc":"SQL, NoSQL và thiết kế database",       "outcomes":"Thiết kế schema, viết query phức tạp"},
            {"id":"patient_data",     "title":"Patient Data Privacy",        "difficulty":"beginner",     "hours":15, "domain":"health", "desc":"Bảo mật dữ liệu y tế và GDPR",         "outcomes":"Hiểu luật bảo mật, áp dụng vào hệ thống y tế"},
            {"id":"digital_health",   "title":"Digital Health Records",      "difficulty":"intermediate", "hours":22, "domain":"health", "desc":"Hệ thống hồ sơ bệnh án điện tử",       "outcomes":"Xây dựng và quản lý EHR system"},
        ]
        for c in courses:
            session.run("""
                CREATE (:Course {
                    id: $id, title: $title, difficulty: $difficulty,
                    hours: $hours, domain: $domain,
                    description: $desc, outcomes: $outcomes
                })
            """, **c)

        # --- Topics ---
        topics = [
            ("python_basics",    [("variables",    "Biến và kiểu dữ liệu"),
                                  ("loops",        "Vòng lặp và điều kiện"),
                                  ("functions",    "Hàm và module")]),
            ("data_analysis",    [("pandas",       "Xử lý dữ liệu với Pandas"),
                                  ("numpy",        "Tính toán số học với NumPy"),
                                  ("statistics",   "Thống kê mô tả")]),
            ("machine_learning", [("supervised",   "Học có giám sát"),
                                  ("unsupervised", "Học không giám sát"),
                                  ("evaluation",   "Đánh giá mô hình")]),
        ]
        for course_id, topic_list in topics:
            for tid, tname in topic_list:
                session.run("CREATE (:Topic {id:$tid, name:$tname})", tid=tid, tname=tname)
                session.run("""
                    MATCH (c:Course {id:$cid}), (t:Topic {id:$tid})
                    CREATE (c)-[:HAS_TOPIC]->(t)
                """, cid=course_id, tid=tid)

        # --- PREREQUISITE relationships ---
        prereqs = [
            ("python_basics", "data_analysis",    0.85),
            ("python_basics", "db_management",    0.75),
            ("data_analysis", "data_viz",         0.90),
            ("data_analysis", "machine_learning", 0.88),
        ]
        for src, dst, score in prereqs:
            session.run("""
                MATCH (a:Course {id:$src}), (b:Course {id:$dst})
                CREATE (a)-[:PREREQUISITE_OF {similarity:$score}]->(b)
            """, src=src, dst=dst, score=score)

        # --- SIMILAR_TO relationships (từ RE algorithm như bài báo) ---
        similarities = [
            ("data_analysis", "data_viz",         0.91),
            ("data_analysis", "machine_learning", 0.86),
            ("data_viz",      "machine_learning", 0.72),
            ("db_management", "data_analysis",    0.68),
            ("patient_data",  "digital_health",   0.89),
            ("data_analysis", "patient_data",     0.55),  # cross-domain
        ]
        for a, b, score in similarities:
            session.run("""
                MATCH (x:Course {id:$a}), (y:Course {id:$b})
                CREATE (x)-[:SIMILAR_TO {similarity:$score}]->(y)
                CREATE (y)-[:SIMILAR_TO {similarity:$score}]->(x)
            """, a=a, b=b, score=score)

        # --- Domain communities (Course -> Domain) ---
        domain_map = {
            "python_basics":"cs", "data_analysis":"cs", "data_viz":"cs",
            "machine_learning":"cs", "db_management":"cs",
            "patient_data":"health", "digital_health":"health",
        }
        for cid, did in domain_map.items():
            session.run("""
                MATCH (c:Course {id:$cid}), (d:Domain {id:$did})
                CREATE (c)-[:BELONGS_TO]->(d)
            """, cid=cid, did=did)

        # --- Learning path (thứ tự gợi ý) ---
        path = ["python_basics", "data_analysis", "data_viz", "machine_learning"]
        for i in range(len(path)-1):
            session.run("""
                MATCH (a:Course {id:$a}), (b:Course {id:$b})
                CREATE (a)-[:NEXT_IN_PATH {order:$order}]->(b)
            """, a=path[i], b=path[i+1], order=i+1)

        print("✅ KG seeded thành công!")
        print(f"   {len(courses)} courses, {len(topics)} course-topics, {len(similarities)} similarity edges")

if __name__ == "__main__":
    seed()
    driver.close()