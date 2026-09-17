
/* WARNING: Removing unreachable block (ram,0x0044a9a2) */

void __fastcall FUN__text__0044a960(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_58 [16];
  undefined4 local_18;
  int local_14;
  undefined1 *local_10;
  undefined *local_c;
  int local_8;
  
  puVar2 = local_58;
  for (iVar1 = 0x15; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  _memset((void *)(param_1 + 0x1ab0),0,0xf0);
  local_18 = 8;
  for (local_14 = 0; local_14 != 8; local_14 = local_14 + 1) {
    local_c = &DAT_00605f18 + local_14 * 0xb0;
    local_10 = (undefined1 *)(local_8 + 0x1ab0 + local_14 * 8);
    *local_10 = 1;
    local_10[1] = 0;
    *(undefined **)(local_10 + 4) = &DAT_00605f18 + local_14 * 0xb0;
  }
  *(undefined1 *)(local_8 + 0x1a99) = 0;
  local_8 = 0x44aa1e;
  FUN__text__0056ce80();
  return;
}

