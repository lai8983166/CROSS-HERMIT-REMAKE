
void __fastcall FUN__text__00451e20(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  int local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  FUN__text__00416370(0x1b8,0x17c,0,"Tactics Scene",
                      (uint)*(byte *)(param_1 + 0x40) << 0x10 | 0xff000000 |
                      (uint)*(byte *)(param_1 + 0x41) << 8 | (uint)*(byte *)(param_1 + 0x42));
  FUN__text__00416370(0x1b8,400,0,"Now Loading ...",
                      (uint)*(byte *)(local_8 + 0x40) << 0x10 | 0xff000000 |
                      (uint)*(byte *)(local_8 + 0x41) << 8 | (uint)*(byte *)(local_8 + 0x42));
  local_8 = 0x451ef8;
  FUN__text__0056ce80();
  return;
}

