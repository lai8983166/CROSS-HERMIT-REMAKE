
void __thiscall FUN_0040d120(int param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (((*(int *)(param_1 + 8) != 0) && (*(int *)(param_1 + 0xc) != 0)) &&
     (*(int *)(param_1 + 0x10) != 0)) {
    local_8 = param_1;
    for (local_10 = 0; local_10 != 0x78; local_10 = local_10 + 1) {
      if (*(int *)(local_8 + 0x14 + param_2 * 0x5a0 + local_10 * 0xc) != 0) {
        (**(code **)(**(int **)(local_8 + 8) + 0xb8))
                  (*(undefined4 *)(local_8 + 8),
                   *(undefined4 *)(local_8 + 0x14 + param_2 * 0x5a0 + local_10 * 0xc),0,0,0);
        __chkesp();
        (**(code **)(**(int **)(local_8 + 0x14 + param_2 * 0x5a0 + local_10 * 0xc) + 0x78))
                  (*(undefined4 *)(local_8 + 0x14 + param_2 * 0x5a0 + local_10 * 0xc),
                   *(undefined4 *)(local_8 + 8));
        local_c = __chkesp();
        if ((local_c != 0) &&
           (iVar2 = FUN_00424f80("ret==((HRESULT)0x00000000L)",
                                 "E:\\CrossHermit\\GAME\\src\\SYSTEM\\DIRECTX\\DXAudio.CPP",
                                 DAT_005ff13c + 0x12,0), iVar2 != 0)) {
          pcVar1 = (code *)swi(3);
          (*pcVar1)();
          return;
        }
        if (*(int *)(local_8 + 0x14 + param_2 * 0x5a0 + local_10 * 0xc) != 0) {
          (**(code **)(**(int **)(local_8 + 0x14 + param_2 * 0x5a0 + local_10 * 0xc) + 8))
                    (*(undefined4 *)(local_8 + 0x14 + param_2 * 0x5a0 + local_10 * 0xc));
          __chkesp();
          *(undefined4 *)(local_8 + 0x14 + param_2 * 0x5a0 + local_10 * 0xc) = 0;
        }
        _memset((void *)(local_8 + 0x14 + param_2 * 0x5a0 + local_10 * 0xc),0,0xc);
      }
    }
    FUN_0040c2a0(param_2);
  }
  local_8 = 0x40d324;
  __chkesp();
  return;
}

