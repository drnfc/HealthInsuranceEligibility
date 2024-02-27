{
  description = "Dr NFC's Personal NixOS System Flake Configuration";

  inputs = {
    #nixos pacages
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    nixpkgs-stable.url = "github:nixos/nixpkgs/nixos-23.05";

    #this makes global colors much easier
    nix-colors.url = "github:misterio77/nix-colors";

    #Nix User Repository
    nur.url = "github:nix-community/NUR";

    doom-emacs = {
      url = "github:nix-community/nix-doom-emacs";
      inputs.nixpkgs.follows = "nixpkgs";
      inputs.emacs-overlay.follows = "emacs-overlay";
    };

    emacs-overlay = { # Emacs Overlays
      url = "github:nix-community/emacs-overlay";
    };

    #Nix-Native Dotfiles Management
    home-manager = {
      url = "github:nix-community/home-manager";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    #An OpenGL wrapper.  Only needed if an application isn't using the same nixpkgs source
    nixgl = {
      url = "github:guibou/nixGL";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    hyprland.url = "github:hyprwm/Hyprland";
    nix-gaming.url = "github:fufexan/nix-gaming";
  };

  outputs =
    { self,
      nixpkgs,
      nixpkgs-stable,
      home-manager,
      nix-colors,
      nur,
      nixgl,
      doom-emacs,
      emacs-overlay,
      hyprland,
      nix-gaming,
      ... } @ inputs:
    let
      configRoot = "$HOME/.dotfiles";
      pkgsForSystem = system: import nixpkgs {
        inherit system;
        config.allowUnfree = true;
        overlays = [
          emacs-overlay.overlay
          (self: super: {
            discord = super.discord.override {
              #withOpenASAR = true;
              #withVencord = true;
            };
          })
          (final: prev: {
            ite8291r3-ctl = final.python3Packages.callPackage ./localRepo/ite8291r3-ctl.nix { };
            rokucli = final.python3Packages.callPackage ./localRepo/rokucli.nix { };
            protonup = final.python3Packages.callPackage ./localRepo/protonup.nix { };
            tessen = final.callPackage ./localRepo/tessen.nix { };
          })
        ];
      };
      theme = {
        uncapped = "dracula";
        capped = "Dracula";
      };

    in {
      nixosConfigurations = {
        NixFTW = nixpkgs.lib.nixosSystem rec{
            system = "x86_64-linux";
            pkgs = pkgsForSystem system;
            specialArgs = {
              inherit theme inputs;
              host = {
                hostName = "NixFTW";
                mainMonitor = "eDP-1";
              };
            };
            modules = [
              inputs.nur.nixosModules.nur
              inputs.hyprland.nixosModules.default
              inputs.home-manager.nixosModules.home-manager
              ./hosts/NixFTW
              ./hosts/laptopDefaults
              ./hosts/configuration.nix
            ];
        };
        renfield = nixpkgs.lib.nixosSystem rec {
            system = "x86_64-linux";
            specialArgs = {
              user = "zack";
              pkgs = pkgsForSystem system;
              inherit theme inputs; 
              host = {
                hostName = "renfield";
                mainMonitor = "eDP-1";
              };
            };
            modules = [
              inputs.nur.nixosModules.nur
              inputs.hyprland.nixosModules.default
              inputs.home-manager.nixosModules.home-manager
              ./hosts/laptopDefaults
              ./hosts/configuration.nix
              ./hosts/renfield
            ];
        };
      };
    };
}

