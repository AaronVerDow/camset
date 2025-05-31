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
            gobject-introspection
            v4l-utils
            ffmpeg
            
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
            echo "  python -m camset.camset      # Run from source"

            # fix for dialog boxes, normally handled by gtk wrapper
            export GSETTINGS_SCHEMA_DIR="${pkgs.gtk3}/share/gsettings-schemas/${pkgs.gtk3.name}/glib-2.0/schemas";
          '';
        };

        apps.default = {
          type = "app";
          program = "${camset}/bin/camset";
        };
      });
} 
