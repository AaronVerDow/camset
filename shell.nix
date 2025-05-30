{ pkgs ? import <nixpkgs> {} }:

let
  camset = pkgs.callPackage ./package.nix {};
in
pkgs.mkShell {
  buildInputs = with pkgs; [
    # Dependencies for building camset
    camset.buildInputs
    camset.nativeBuildInputs
    
    # Additional development tools
    python3
    python3Packages.pip
    python3Packages.setuptools
    v4l-utils
    
    # For testing
    xorg.xhost  # For X11 forwarding if needed
  ];
  
  shellHook = ''
    echo "Camset development environment"
    echo "=========================="
    echo "Available commands:"
    echo "  nix-build -f package.nix  # Build the package"
    echo "  python setup.py install   # Install locally for development"
    echo "  python -m camset.camset   # Run camset directly"
    echo ""
    echo "To test the GUI, make sure you have a camera connected and X11 forwarding enabled if using SSH."
  '';
} 