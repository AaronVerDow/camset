{
  description = "Camset - GUI for Video4Linux adjustments of webcams";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        camset = pkgs.callPackage ./package.nix {};
      in
      {
        packages = {
          default = camset;
          camset = camset;
        };

        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            # Build dependencies
            python3
            python3Packages.setuptools
            python3Packages.pygobject3
            python3Packages.opencv-python
            gobject-introspection
            v4l-utils
            
            # Development tools
            python3Packages.pip
            python3Packages.pytest
            
            # GTK runtime
            gtk3
            glib
            
            # For X11 apps
            xorg.xhost
          ];
          
          shellHook = ''
            echo "🎥 Camset Development Environment"
            echo "================================"
            echo ""
            echo "Build and test commands:"
            echo "  nix build                    # Build the package"
            echo "  nix run                      # Run camset directly"
            echo "  python setup.py develop      # Install in development mode"
            echo "  python -m camset.camset      # Run from source"
            echo ""
            echo "Make sure you have:"
            echo "  - A webcam connected (check with: v4l2-ctl --list-devices)"
            echo "  - X11 display available (for GUI)"
            echo ""
          '';
        };

        apps.default = {
          type = "app";
          program = "${camset}/bin/camset";
        };
      });
} 