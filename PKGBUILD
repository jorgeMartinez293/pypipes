pkgname=pypipes-git

pkgver=rX
pkgrel=1
pkgdesc="A python recreation of 'pipes.sh' with a few custom arguments"
arch=('any')
url="https://github.com/jorgeMartinez293/pypipes"
license=('MIT') 
depends=('python')
provides=("pypipes")
conflicts=("pipes-py") 

source=("${pkgname}::git+${url}.git")
sha256sums=('SKIP') 

pkgver() {
  cd "${srcdir}/${pkgname}"
  printf "r%s.%s" "$(git rev-list --count HEAD)" "$(git describe --long --always | sed 's/\([^-]*-\)//g')"
}

package() {
  install -Dm755 "${srcdir}/${pkgname}/pipes.py" "${pkgdir}/usr/bin/pypipes" 
}
