import { useState, useEffect } from "react";
import { getCourses } from "../api";

const DIFFICULTY_LABEL = {
  beginner: "Beginner",
  intermediate: "Intermediate",
  advanced: "Advanced"
};

const DIFFICULTY_COLOR = {
  beginner: "text-green-400",
  intermediate: "text-yellow-400",
  advanced: "text-red-400"
};

export default function RecommendationCard({
  onSelectCourse,
  selectedCourse
}) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getCourses()
      .then(res => setData(res))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="text-zinc-400 text-sm">
        Đang tải learning path...
      </div>
    );
  }

  if (!data) {
    return (
      <div className="text-red-400 text-sm">
        Không thể tải dữ liệu từ backend.
      </div>
    );
  }

  const { path, courses } = data;

  const orderedCourses = path
    .map(id => courses.find(c => c.id === id))
    .filter(Boolean);

  return (
    <div className="space-y-3 pr-2">
      {orderedCourses.map((course, index) => (
        <button
          key={course.id}
          onClick={() => onSelectCourse?.(course)}
          className={`
            w-full
            text-left
            rounded-2xl
            border
            p-4
            transition-all
            duration-200

            ${
              selectedCourse?.id === course.id
                ? `
                  border-indigo-500
                  bg-indigo-500/10
                `
                : `
                  border-zinc-700
                  bg-zinc-800
                  hover:bg-zinc-700
                `
            }
          `}
        >
          <div className="flex items-start gap-3">
            <div
              className="
                w-8
                h-8
                rounded-full
                bg-zinc-700
                flex
                items-center
                justify-center
                text-xs
                font-semibold
                shrink-0
              "
            >
              {index + 1}
            </div>

            <div className="flex-1 min-w-0">
              <h3
                className="
                  font-medium
                  text-white
                  text-sm
                  truncate
                "
              >
                {course.title}
              </h3>

              <div
                className="
                  mt-1
                  flex
                  items-center
                  gap-2
                  text-xs
                "
              >
                <span className="text-zinc-400">
                  {course.domain || "Computer Science"}
                </span>

                <span className="text-zinc-600">
                  •
                </span>

                <span
                  className={
                    DIFFICULTY_COLOR[
                      course.difficulty
                    ]
                  }
                >
                  {
                    DIFFICULTY_LABEL[
                      course.difficulty
                    ]
                  }
                </span>
              </div>

              <div
                className="
                  mt-2
                  text-xs
                  text-zinc-500
                "
              >
                {course.hours} giờ học
              </div>

              {selectedCourse?.id === course.id && (
                <div
                  className="
                    mt-3
                    text-xs
                    font-medium
                    text-indigo-400
                  "
                >
                  Đang thảo luận với DoDo
                </div>
              )}
            </div>
          </div>
        </button>
      ))}
    </div>
  );
}