import { createClient } from "@/utils/supabase/server";
import { currentUser } from "@clerk/nextjs/server";
import React from "react";
import { redirect } from "next/navigation";
import ProfileSummary from "./_components/ProfileSummary";
import ProfileForm from "./_components/ProfileForm";

export const metadata = {
  title: "Profile | EduAI",
  description: "Manage your student profile and learning preferences",
};

export default async function Page() {
  // get the current user
  const cUser = await currentUser();

  if (!cUser) {
    redirect("/");
  }

  // check if this user exists in the database
  const supabase = await createClient();

  const { data: user } = await supabase
    .from("users")
    .select("*")
    .eq("sub", cUser?.id)
    .single();

  if (!user) {
    // create a new user in the database
    const { data, error } = await supabase.from("users").insert({
      sub: cUser?.id,
      email: cUser?.emailAddresses[0]?.emailAddress,
      first_name: cUser?.firstName,
      last_name: cUser?.lastName,
    });
    console.log("created user", data, error);
  }

  const { data: studentProfile } = await supabase
    .from("student_profile")
    .select("*")
    .eq("user_id", user?.id)
    .single();

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      <div className="max-w-4xl mx-auto py-8 px-4">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Profile Settings
          </h1>
          <p className="text-gray-600">
            Manage your profile information and learning preferences
          </p>
        </div>

        {/* Profile Summary */}
        <ProfileSummary user={user} studentProfile={studentProfile} />

        {/* Profile Form */}
        <ProfileForm user={user} studentProfile={studentProfile} />
      </div>
    </div>
  );
}
