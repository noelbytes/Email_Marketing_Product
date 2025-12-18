describe('Constellation smoke test', () => {
  it('allows a marketer to sign in and view mission control', () => {
    const corsHeaders = {
      'access-control-allow-origin': '*',
      'access-control-allow-methods': 'GET,POST,PUT,DELETE,OPTIONS',
      'access-control-allow-headers': 'authorization,content-type',
    }

    cy.intercept('OPTIONS', '**/api/auth/login', {
      statusCode: 204,
      headers: corsHeaders,
    })

    cy.intercept('GET', '**/api/healthz', {
      statusCode: 200,
      headers: corsHeaders,
      body: {
        status: 'ok',
        service: 'email-marketing-api',
        version: '0.1.0',
        timestamp: new Date().toISOString(),
      },
    })

    cy.intercept('POST', '**/api/auth/login', {
      statusCode: 200,
      headers: corsHeaders,
      body: {
        access_token: 'test-token',
        token_type: 'bearer',
        user: {
          id: 1,
          email: 'ops@example.com',
          first_name: 'Ops',
          last_name: 'User',
          organization_id: 1,
          roles: ['org-admin'],
        },
        roles: ['org-admin'],
        permissions: ['*'],
      },
    })

    cy.visit('/login')
    cy.get('input[name="email"]').type('ops@example.com')
    cy.get('input[name="password"]').type('marketing-platform')
    cy.get('input[name="organization"]').type('Orbit Collective')
    cy.contains('button', 'Take me to Mission Control').click()
    cy.url().should('include', '/app')
    cy.contains('Lifecycle Command')
    cy.contains('Mission Control')
  })
})
