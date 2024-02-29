{
  inputs = {
    nixpkgs = {
      url = "github:nixos/nixpkgs/nixos-unstable";
    };
    flake-utils = {
      url = "github:numtide/flake-utils";
    };
  };

  description = "Data Science Dev Shell";

  outputs = { nixpkgs, flake-utils, ... }: flake-utils.lib.eachDefaultSystem (system:
    let
      pkgs = import nixpkgs {
        inherit system;
      };
    in rec {
      devShell = pkgs.mkShell {
        buildInputs = with pkgs; [
          qt5.full #needed for me to render plots
          (python311.withPackages (python-pkgs: with python-pkgs; [
            jupyter
            matplotlib
            numpy
            pandas
          ]))
          zsh
        ];
        shellHook = ''
          zsh
          exit
        '';
      };
    }); 
}
