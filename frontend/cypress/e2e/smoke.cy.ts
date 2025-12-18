describe('Constellation smoke test', () => {
  it('allows a marketer to sign in and view mission control', () => {
    cy.visit('/login')
    cy.get('input[name="email"]').type('ops@example.com')
    cy.get('input[name="password"]').type('marketing-platform')
    cy.get('input[name="organization"]').type('Orbit Collective')
    cy.contains('button', 'Take me to Mission Control').click()
    cy.contains('Mission Control')
    cy.contains('Orbit Collective')
  })
})
