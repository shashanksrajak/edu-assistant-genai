"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { User, BookOpen, GraduationCap } from "lucide-react";

interface User {
  id: string;
  first_name: string;
  last_name: string;
  email: string;
  user_type?: string;
}

interface StudentProfile {
  id: string;
  user_id: string;
  grade_level: string;
  language: string;
}

interface ProfileSummaryProps {
  user: User;
  studentProfile: StudentProfile | null;
}

export default function ProfileSummary({
  user,
  studentProfile,
}: ProfileSummaryProps) {
  return (
    <Card className="mb-8">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <User className="w-5 h-5" />
          Profile Summary
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* User Info */}
        <div className="flex items-center gap-4">
          <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
            <span className="text-white text-xl font-bold">
              {user.first_name?.[0]}
              {user.last_name?.[0]}
            </span>
          </div>
          <div>
            <h2 className="text-xl font-semibold text-gray-900">
              {user.first_name} {user.last_name}
            </h2>
            <p className="text-gray-600">{user.email}</p>
          </div>
        </div>

        {studentProfile ? (
          <div className="grid md:grid-cols-2 gap-6">
            {/* Grade Level */}
            <div className="bg-blue-50 p-4 rounded-lg">
              <div className="flex items-center gap-2 mb-2">
                <GraduationCap className="w-4 h-4 text-blue-600" />
                <h3 className="font-medium text-blue-900">Grade Level</h3>
              </div>
              <p className="text-blue-700">{studentProfile.grade_level}</p>
            </div>

            {/* Language */}
            <div className="bg-green-50 p-4 rounded-lg">
              <div className="flex items-center gap-2 mb-2">
                <BookOpen className="w-4 h-4 text-green-600" />
                <h3 className="font-medium text-green-900">Language</h3>
              </div>
              <p className="text-green-700">{studentProfile.language}</p>
            </div>
          </div>
        ) : (
          <div className="bg-orange-50 border border-orange-200 rounded-lg p-4">
            <div className="flex items-center gap-2 mb-2">
              <div className="w-8 h-8 bg-orange-500 rounded-full flex items-center justify-center">
                <span className="text-white text-sm">!</span>
              </div>
              <h3 className="font-medium text-orange-900">
                Profile Incomplete
              </h3>
            </div>
            <p className="text-orange-700 text-sm">
              Complete your student profile below to personalize your learning
              experience.
            </p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
