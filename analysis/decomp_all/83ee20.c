
void FUN__text1__0083ee20(int param_1)

{
  undefined4 local_8;
  
  local_8 = *(uint *)(*(int *)(param_1 + 0x1c) + 0x14);
  if (*(uint *)(param_1 + 0x10) < local_8) {
    local_8 = *(uint *)(param_1 + 0x10);
  }
  if (local_8 != 0) {
    FUN__text1__00848490
              (*(undefined4 *)(param_1 + 0xc),*(undefined4 *)(*(int *)(param_1 + 0x1c) + 0x10),
               local_8);
    *(uint *)(param_1 + 0xc) = *(int *)(param_1 + 0xc) + local_8;
    *(uint *)(*(int *)(param_1 + 0x1c) + 0x10) = *(int *)(*(int *)(param_1 + 0x1c) + 0x10) + local_8
    ;
    *(uint *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + local_8;
    *(uint *)(param_1 + 0x10) = *(int *)(param_1 + 0x10) - local_8;
    *(uint *)(*(int *)(param_1 + 0x1c) + 0x14) = *(int *)(*(int *)(param_1 + 0x1c) + 0x14) - local_8
    ;
    if (*(int *)(*(int *)(param_1 + 0x1c) + 0x14) == 0) {
      *(undefined4 *)(*(int *)(param_1 + 0x1c) + 0x10) =
           *(undefined4 *)(*(int *)(param_1 + 0x1c) + 8);
    }
  }
  return;
}

