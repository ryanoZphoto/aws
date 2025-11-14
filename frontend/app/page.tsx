export default function Home() {
  return (
    <main className="min-h-screen p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-4xl font-bold mb-8">
          AWS Service Automation & Control Platform
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Automated daily checks and task execution for all AWS services
        </p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-2xl font-semibold mb-4">Create Tasks</h2>
            <p className="text-gray-600">
              Set up automated checks for any AWS service with custom operations and schedules.
            </p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-2xl font-semibold mb-4">Monitor Results</h2>
            <p className="text-gray-600">
              View execution results, track success rates, and get notified of issues.
            </p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-2xl font-semibold mb-4">Manage Credentials</h2>
            <p className="text-gray-600">
              Securely store and manage AWS credentials with encryption at rest.
            </p>
          </div>
        </div>
      </div>
    </main>
  )
}
