"use client";

import React, { useState, useEffect } from "react";
import { GraduationCap, Calendar, Clock, AlertCircle } from "lucide-react";

interface ExamEntry {
  id: string;
  course_code: string;
  subject_name: string;
  category: string;
  exam_date: string | null;
  start_time: string | null;
  end_time: string | null;
  status: string;
}

interface ExamResponse {
  semester_exams: ExamEntry[];
}

export default function SemesterExamRadar() {
  const [exams, setExams] = useState<ExamResponse | null>(null);

  useEffect(() => {
    fetch("/api/exams/all")
      .then(res => res.json())
      .then(data => setExams(data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div className="bg-zinc-900/60 border border-zinc-800 rounded-xl p-5 backdrop-blur-sm flex flex-col h-full">
      <div className="flex items-center gap-2 pb-4 border-b border-zinc-800/80 mb-4">
        <div className="p-1.5 rounded-lg bg-sky-500/10 border border-sky-500/20 text-sky-400">
          <GraduationCap className="w-4 h-4" />
        </div>
        <div>
          <h2 className="text-sm font-semibold text-zinc-100 flex items-center gap-2">
            December 2026 Semester Examination Radar
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-sky-500/10 border border-sky-500/30 text-sky-400">
              Official Timetable
            </span>
          </h2>
          <p className="text-xs text-zinc-400">Year I University Semester Examinations (10:00 AM – 01:00 PM)</p>
        </div>
      </div>

      <div className="space-y-3 overflow-y-auto flex-1">
        {exams?.semester_exams?.map((exam) => {
          const isDateSet = exam.status === "SCHEDULED";
          return (
            <div
              key={exam.id}
              className="p-3 bg-zinc-950/40 border border-zinc-800/80 rounded-lg flex items-center justify-between"
            >
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-semibold text-zinc-200">{exam.subject_name}</span>
                  <span className="text-[10px] font-mono text-zinc-500">({exam.course_code})</span>
                </div>
                <div className="flex items-center gap-3 text-[10px] font-mono text-zinc-400 mt-1">
                  {isDateSet ? (
                    <>
                      <span className="flex items-center gap-1 text-sky-400">
                        <Calendar className="w-3 h-3" />
                        {exam.exam_date}
                      </span>
                      <span className="flex items-center gap-1">
                        <Clock className="w-3 h-3" />
                        {exam.start_time} - {exam.end_time}
                      </span>
                    </>
                  ) : (
                    <span className="flex items-center gap-1 text-zinc-500">
                      <AlertCircle className="w-3 h-3" />
                      Date Not Provided
                    </span>
                  )}
                </div>
              </div>

              <div>
                <span className={`text-[10px] font-mono px-2 py-1 rounded border ${
                  isDateSet ? 'bg-sky-500/10 text-sky-400 border-sky-500/20' : 'bg-zinc-800 text-zinc-400 border-zinc-700'
                }`}>
                  {exam.status}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
