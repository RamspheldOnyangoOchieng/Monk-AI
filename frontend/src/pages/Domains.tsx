import React, { useState } from 'react';
import { Button } from '../components/ui/button';

interface Domain {
  id: string;
  name: string;
  description: string;
  status: 'active' | 'inactive';
}

const Domains: React.FC = () => {
  const [domains, setDomains] = useState<Domain[]>([
    {
      id: '1',
      name: 'Web Development',
      description: 'Frontend and backend web development services',
      status: 'active'
    },
    {
      id: '2',
      name: 'Mobile Development',
      description: 'iOS and Android mobile application development',
      status: 'active'
    },
    {
      id: '3',
      name: 'AI/ML',
      description: 'Artificial Intelligence and Machine Learning solutions',
      status: 'active'
    }
  ]);

  const handleStatusToggle = (id: string) => {
    setDomains(domains.map(domain => 
      domain.id === id 
        ? { ...domain, status: domain.status === 'active' ? 'inactive' : 'active' }
        : domain
    ));
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-900">Domains</h1>
        <Button variant="default">Add New Domain</Button>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {domains.map(domain => (
          <div key={domain.id} className="bg-white rounded-lg shadow p-6">
            <div className="flex justify-between items-start">
              <div>
                <h3 className="text-lg font-semibold text-gray-900">{domain.name}</h3>
                <p className="mt-1 text-sm text-gray-500">{domain.description}</p>
              </div>
              <Button
                variant={domain.status === 'active' ? 'default' : 'secondary'}
                onClick={() => handleStatusToggle(domain.id)}
              >
                {domain.status === 'active' ? 'Active' : 'Inactive'}
              </Button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Domains;
