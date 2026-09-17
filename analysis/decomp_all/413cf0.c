
void __fastcall FUN__text__00413cf0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_68 [16];
  int local_28;
  int local_24;
  int local_20;
  int local_1c;
  int local_18;
  int local_14;
  undefined4 local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_68;
  for (iVar1 = 0x19; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*(int *)(param_1 + 0xb20c) != 0) {
    local_8 = param_1;
    _memset((void *)(param_1 + 0xb224),0,0x10);
    (**(code **)(**(int **)(local_8 + 0xb20c) + 0x18))(*(undefined4 *)(local_8 + 0xb20c),0);
    local_28 = FUN__text__0056ce80();
    for (local_20 = 0; *(int *)(&DAT_005ff490 + local_20 * 4) != 0; local_20 = local_20 + 1) {
      for (local_24 = 0; local_24 != local_28; local_24 = local_24 + 1) {
        (**(code **)(**(int **)(local_8 + 0xb20c) + 0x1c))
                  (*(undefined4 *)(local_8 + 0xb20c),0,local_24,&local_18);
        local_1c = FUN__text__0056ce80();
        if (local_1c < 0) goto LAB__text__00413e39;
        if (((local_c == *(int *)(&DAT_005ff490 + local_20 * 4)) &&
            (local_18 == *(int *)(local_8 + 0xb278))) && (local_14 == *(int *)(local_8 + 0xb27c))) {
          *(int *)(local_8 + 0xb224) = local_18;
          *(int *)(local_8 + 0xb228) = local_14;
          *(undefined4 *)(local_8 + 0xb22c) = local_10;
          *(int *)(local_8 + 0xb230) = local_c;
          goto LAB__text__00413e39;
        }
      }
    }
  }
LAB__text__00413e39:
  local_8 = 0x413e46;
  FUN__text__0056ce80();
  return;
}

