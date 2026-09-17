
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __fastcall FUN__text__005361a5(int param_1)

{
  undefined4 uVar1;
  
  uVar1 = _DAT_005d0e44;
  if ((*(int *)(param_1 + 4) != 0x32545844) && (*(int *)(param_1 + 4) != 0x33545844)) {
    uVar1 = _DAT_005d0e38;
  }
  *(undefined4 *)(param_1 + 0x106c) = uVar1;
  *(float *)(param_1 + 0x1070) = 1.0 / *(float *)(param_1 + 0x106c);
  *(float *)(param_1 + 0x1c) =
       (float)(int)ROUND(*(float *)(param_1 + 0x1c) * _DAT_005d0e40 + _DAT_005d0a3c) * _DAT_005d0e74
  ;
  *(float *)(param_1 + 0x20) =
       (float)(int)ROUND(*(float *)(param_1 + 0x20) * _DAT_005d0e3c + _DAT_005d0a3c) * _DAT_005d0e70
  ;
  *(float *)(param_1 + 0x24) =
       (float)(int)ROUND(*(float *)(param_1 + 0x24) * _DAT_005d0e40 + _DAT_005d0a3c) * _DAT_005d0e74
  ;
  *(float *)(param_1 + 0x28) =
       (float)(int)ROUND(*(float *)(param_1 + 0x106c) * *(float *)(param_1 + 0x28) + _DAT_005d0a3c)
       * *(float *)(param_1 + 0x1070);
  return;
}

