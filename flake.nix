{
  # OmniPython dev environment — nix owns python + uv, uv.lock owns packages.
  description = "OmniPython-template development environment";

  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forAllSystems = f: nixpkgs.lib.genAttrs systems (s: f nixpkgs.legacyPackages.${s});
    in
    {
      devShells = forAllSystems (pkgs: {
        default = pkgs.mkShell {
          packages = with pkgs; [
            python313
            uv
            pyright
            git
          ];
          shellHook = ''
            echo "OmniPython: uv $(uv --version | cut -d' ' -f2) — run 'uv sync' then 'make ci'"
          '';
        };
      });
    };
}
